from __future__ import annotations

from typing import Union, IO
import yaml


class System(object):

    class Affix(object):

        @property
        def is_prefix(self) -> bool:
            return self.acronym.startswith(':')

        def __init__(self, name, acronym):
            self.name:str = name
            self.acronym:str = acronym

    class Info(object):

        def __init__(self, data:dict):
            # Typedefs
            self.users:list[str]
            self.initiator:Union[str, None]
            self.namesake:Union[str, None]
            self.notes:Union[str, None]
            self.succeeded_by:Union[tuple[str, int], None]
            # Attributes
            self.users         = data['users']
            self.initiator     = data.get('initiator',    None)
            self.namesake      = data.get('namesake',     None)
            self.notes         = data.get('notes',        None)
            self.succeeded_by  = data.get('_succeededBy', None)

    @property
    def info(self) -> System.Info:
        if not self._info: self._info = self._init_info()
        return self._info

    @property
    def eras(self) -> Union[dict[int, System.Affix], None]:
        if not self._eras: self._eras = self._init_eras()
        return self._eras

    @property
    def affix_positive(self) -> System.Affix:
        if not self._affix_positive: self._affix_positive = self._init_affix_positive()
        return self._affix_positive

    @property
    def affix_negative(self) -> System.Affix:
        if not self._affix_negative: self._affix_negative = self._init_affix_negative()
        return self._affix_negative

    def get_year(self, year:int) -> str:

        is_positive = year > 0

        use_eras:bool
        universal_affix:bool
        affix:System.Affix = None
        if self.eras:
            use_eras = True
            universal_affix = False
            for era_start, era_affix in self.eras.items():
                if year > era_start:
                    year  = year - era_start
                    affix = era_affix
                    break
            if not affix: affix = self.affix_positive
        else:
            use_eras = False
            universal_affix = self.affix_negative is None
            if universal_affix or is_positive:
                affix = self.affix_positive
            else:
                affix = self.affix_negative

        if not (use_eras or is_positive or universal_affix):
            year = abs(year)

        return f'{year} {affix.acronym}' if not affix.is_prefix else f'{affix.acronym[1:]} {year}'

    def _init_info(self):
        return System.Info(self.__data['info'])

    def _init_eras(self):
        eras = self.__data.get('eras', None)
        if not eras: return dict()

        result = dict()

        pair:dict
        for pair in eras:
            year = next(iter(pair))
            result[year] = self.__init_affix(pair[year])

        return result

    def __init_affix(self, data):
        return System.Affix(*data)

    def _init_affix_positive(self):
        _key = 'affixPositive'

        affix = self.__data.get(_key, None)
        if not affix:
            raise ValueError(f"{self.id} is missing '{_key}' field")

        return self.__init_affix(tuple(affix))

    def _init_affix_negative(self):
        affix = self.__data.get('affixNegative', None)
        return self.__init_affix(tuple(affix)) if affix else None

    def __init__(self, data:dict):
        self.__data = data
        # Attributes:
        self.id:str              = self.__data['id']
        self.name:str            = self.__data['name']
        self.reference_year:int  = self.__data['referenceYear']
        # Properties:
        self._info = None
        self._eras = None
        self._affix_positive = None
        self._affix_negative = None

class Index(object):

    @classmethod
    def from_yaml(cls, s:str) -> Index:
        return Index(yaml.load(s, Loader=yaml.FullLoader))

    @classmethod
    def from_file(cls, fp:IO[str]) -> Index:
        return Index.from_yaml(fp.read())

    @property
    def systems(self) -> list[System]:
        if not self._systems: self._systems = self._init_systems()
        return self._systems

    @property
    def ids(self) -> list[str]:
        return self.__document['_index']

    def get_system(self, id:str) -> Union[System, None]:
        try:
            system = next(
                system for system in self.systems if system.id == id.lower()
            )
        except StopIteration:
            system = None
        return system

    def _init_systems(self):
        return [System(i) for i in self.__document['data']]

    def __init__(self, document:dict):
        self.__document = {'_index': document['_index'], 'data': document['data']}
        # Properties:
        self._systems:list[System] = None

    def __iter__(self) -> System:
        for system in self.systems:
            yield system
