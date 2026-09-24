"""Reference in-memory adapter used only for deterministic tests and examples."""
from dataclasses import replace
from threading import RLock
from contextlib import contextmanager
from copy import deepcopy
from uuid import UUID
from .errors import *
from .models import *
from .normalization import name_key

class MemoryStore:
    def __init__(self, audit_sink=None):
        self._lock = RLock(); self.persons={}; self.identifiers={}; self.contacts={}; self.addresses={}; self.genders={}; self.identities={}; self.tax_identifiers={}; self.tax_profiles={}; self.tax_categories={}; self.links={}; self.audit=[]; self.audit_sink=audit_sink
    def _person(self, org, pid):
        person=self.persons.get((org,pid))
        if person is None: raise NotFoundError()
        return person
    def _bump(self, org, pid, expected):
        p=self._person(org,pid)
        if p.version != expected: raise VersionConflictError()
        updated=replace(p, version=p.version+1, updated_at=utcnow()); self.persons[(org,pid)]=updated; return updated
    def _event(self, event):
        if self.audit_sink: self.audit_sink.append(event)
        self.audit.append(event)
    @contextmanager
    def transaction(self):
        with self._lock:
            snapshot=(deepcopy(self.persons),deepcopy(self.identifiers),deepcopy(self.contacts),deepcopy(self.addresses),deepcopy(self.genders),deepcopy(self.identities),deepcopy(self.tax_identifiers),deepcopy(self.tax_profiles),deepcopy(self.tax_categories),deepcopy(self.links),deepcopy(self.audit))
            try: yield
            except Exception:
                self.persons,self.identifiers,self.contacts,self.addresses,self.genders,self.identities,self.tax_identifiers,self.tax_profiles,self.tax_categories,self.links,self.audit=snapshot
                raise
    def create_person(self, person, link):
        with self._lock:
            key=(person.organization_id,person.person_id)
            if key in self.persons: raise ValidationError()
            self.persons[key]=person; self.links[link.link_id]=link; return person
    def get_person(self, org, pid): return self.persons.get((org,pid))
    def list_persons(self, org, limit, after=None):
        with self._lock:
            items=sorted((p for (o,_),p in self.persons.items() if o==org), key=lambda p:str(p.person_id))
            if after: items=[p for p in items if str(p.person_id)>str(after)]
            return items[:limit]
    def update_person(self, person, expected_version):
        with self._lock:
            current=self._person(person.organization_id,person.person_id)
            if current.version != expected_version: raise VersionConflictError()
            updated=replace(person, version=current.version+1, created_at=current.created_at, updated_at=utcnow())
            self.persons[(person.organization_id,person.person_id)]=updated; return updated
    def add_identifier(self, identifier, expected_version):
        with self._lock:
            key=(identifier.organization_id,identifier.country_code,identifier.document_type,identifier.value_normalized)
            if any((i.organization_id,i.country_code,i.document_type,i.value_normalized)==key for i in self.identifiers.values()):
                raise DuplicateIdentifierError()
            self._bump(identifier.organization_id,identifier.person_id,expected_version)
            self.identifiers[identifier.identifier_id]=identifier; return identifier
    def list_identifiers(self, org, pid): return [i for i in self.identifiers.values() if i.organization_id==org and i.person_id==pid]
    def add_contact(self, contact, expected_version):
        with self._lock:
            self._bump(contact.organization_id,contact.person_id,expected_version)
            if contact.is_primary:
                for key,c in list(self.contacts.items()):
                    if c.organization_id==contact.organization_id and c.person_id==contact.person_id and c.kind==contact.kind and c.is_primary:
                        self.contacts[key]=replace(c,is_primary=False,updated_at=utcnow())
            self.contacts[contact.contact_id]=contact; return contact
    def list_contacts(self, org, pid): return [c for c in self.contacts.values() if c.organization_id==org and c.person_id==pid]
    def add_address(self, address, expected_version):
        with self._lock:
            self._bump(address.organization_id,address.person_id,expected_version)
            if address.is_primary:
                for k,a in list(self.addresses.items()):
                    if a.organization_id==address.organization_id and a.person_id==address.person_id and a.address_type==address.address_type:
                        self.addresses[k]=replace(a,is_primary=False,updated_at=utcnow())
            self.addresses[address.address_id]=address; return address
    def list_addresses(self, org, pid): return [a for a in self.addresses.values() if a.organization_id==org and a.person_id==pid]
    def save_gender(self, option): self.genders[(option.organization_id,option.code)]=option; return option
    def list_genders(self, org): return [g for (o,_),g in self.genders.items() if o==org and g.active]
    def save_identity(self, identity):
        with self._lock:
            for existing in self.identities.values():
                if existing.organization_id==identity.organization_id and existing.person_id==identity.person_id and existing.status=="active":
                    if existing.core_user_id==identity.core_user_id and existing.external_subject==identity.external_subject: return existing
                    raise IdentityConflictError()
            self.identities[identity.identity_id]=identity; return identity
    def get_identity(self, org, pid): return next((i for i in self.identities.values() if i.organization_id==org and i.person_id==pid and i.status=="active"),None)
    def remove_identity(self, org, pid):
        i=self.get_identity(org,pid)
        if i: self.identities[i.identity_id]=replace(i,status="inactive",updated_at=utcnow())
        return i
    def save_tax_identifier(self, item):
        if any(i.organization_id==item.organization_id and i.country_code==item.country_code and i.identifier_type==item.identifier_type and i.value_normalized==item.value_normalized for i in self.tax_identifiers.values()): raise DuplicateIdentifierError()
        self.tax_identifiers[item.tax_identifier_id]=item; return item
    def list_tax_identifiers(self, org, pid): return [i for i in self.tax_identifiers.values() if i.organization_id==org and i.person_id==pid]
    def save_tax_profile(self, profile): self.tax_profiles[(profile.organization_id,profile.person_id,profile.country_code)]=profile; return profile
    def get_tax_profile(self, org, pid, country): return self.tax_profiles.get((org,pid,country))
    def save_tax_category(self, category): self.tax_categories[(category.country_code,category.code,category.valid_from)]=category; return category
    def list_tax_categories(self, country, on_date): return [c for c in self.tax_categories.values() if c.country_code==country and c.valid_from<=on_date and (c.valid_to is None or on_date<=c.valid_to)]
    def candidates(self, org, keys, limit):
        out=[]
        for p in self.persons.values():
            if p.organization_id!=org: continue
            pkeys={name_key(p.display_name),name_key(p.given_names or ""),name_key(p.family_names or "")}
            matches=pkeys & keys
            for i in self.identifiers.values():
                if i.organization_id==org and i.person_id==p.person_id and i.value_normalized in keys: matches.add("identifier")
            for c in self.contacts.values():
                if c.organization_id==org and c.person_id==p.person_id and c.value_normalized in keys: matches.add(c.kind)
            for reason in sorted(matches): out.append((p,reason))
        return out[:limit]
