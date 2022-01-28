from os import listxattr
from Artesian import _ClientsExecutor
from Artesian._ClientsExecutor import RequestExecutor
from Artesian._Query.Query import _Query
from Artesian._Query.QueryParameters.VersionedQueryParameters import VersionedQueryParameters
from Artesian._Query.Config.ExtractionRangeConfig import ExtractionRangeConfig
from Artesian._Query.Config.VersionSelectionType import VersionSelectionType
from Artesian._Configuration.DefaultPartitionStrategy import DefaultPartitionStrategy
from Artesian._Query.Config.Granularity import Granularity
import urllib
from __future__ import annotations

class _VersionedQuery(_Query):
    __routePrefix = "vts"
    def __init__(self, client: _ClientsExecutor, requestExecutor: RequestExecutor, partitionStrategy: DefaultPartitionStrategy) -> None:
        """ Inits _VersionedQuery 

            Args:
            
                client 

                requestExecutor

                partitionStrategy. """

        queryParameters = VersionedQueryParameters(None,ExtractionRangeConfig(), None, None, None, None, None, None, None) 
        _Query.__init__(self, client, requestExecutor, queryParameters)
        self.__partition= partitionStrategy

    def forMarketData(self, ids: int) -> _VersionedQuery:
        """ Set the list of marketdata to be queried.

            Args:
                ids: list of marketdata id's to be queried. E.g.: 100000xxx
        """
        super()._forMarketData(ids)
        return self
    def forFilterId(self, filterId: int) -> _VersionedQuery:
        """ Sets the list of filtered marketdata id to be queried
            
            Args:
                filterId: list of marketdata filtered by id"""
        super()._forFilterId(filterId)
        return self
    def inTimeZone(self, tz: str) -> _VersionedQuery:
        """ Gets the Versioned Query in a specific TimeZone in IANA format.

            Args:
                timezone: "UTC","CET","Europe/Istanbul"
        """
        super()._inTimezone(tz)
        return self
    def inAbsoluteDateRange(self, start: str, end: str) -> _VersionedQuery:
        """ Gets the Versioned Query in an absolute date range window. 
            The Absolute Date Range is in ISO8601 format.
        
            Args:
                start: the date start of the range of extracted timeserie, in ISO format. (ex. "2022-01-01")
                end:  the EXCLUSIVE date end of the range of extracted timeserie, in ISO format. (ex. "2022-01-01")
        """
        super()._inAbsoluteDateRange(start, end)
        return self
    def inRelativePeriodRange(self, pStart: str, pEnd=None) -> _VersionedQuery:
        """ Gets the Versioned Query in a relative period range time window.
        
            Args:
                pStart: the relative period start of the range of extracted timeseries. (ex. "P--3D")
                pEnd: the relative period end of the range of the extracted timeseries. (ex. "P10D") 
        """


        super()._inRelativePeriodRange(pStart, pEnd)
        return self
    def inRelativePeriod(self, extractionPeriod: str) -> _VersionedQuery:
        """ Gets the Versioned Query in a relative period of a time window.
        
            Args:
                extractionPeriod: the relative period of extracted timeseries. (ex. "P5D")
        """
        super()._inRelativePeriod(extractionPeriod)
        return self
    def inRelativeInterval(self, relativeInterval: str) -> _VersionedQuery:
        """ Gets the Relative Interval considers a specific interval of time window.
        
            Args:
                relativeInterval: the relative interval of extracted timeseries. (ex. "RelativeInterval.ROLLING_WEEK" or "RelativeInterval.ROLLING_MONTH") 
        """
        super()._inRelativeInterval(relativeInterval)
        return self
    def withTimeTransform(self, tr: str) -> _VersionedQuery:
        """ Gets the Versioned query in a specific Time Transform.
        
            Args:
                tr: "Custom","GASDAY66","THERMALYEAR"."""
        self._queryParameters.transformId = tr
        return self
    def inGranularity(self, granularity: Granularity) -> _VersionedQuery:
        """ Gets the Versioned Query in a specific Granularity.
        
            Args:
                granularity: "TenMinute", "FifteenMinute", "Hour", "Year"
        """
        self._queryParameters.granularity = granularity
        return self
    def forMUV(self) -> _VersionedQuery:
        """ Gets the timeseries of the most updated version of each timepoint of a versioned timeseries.
            """
        self._queryParameters.versionSelectionType = VersionSelectionType.MUV
        return self
    def forLastOfDays(self, start: str, end=None) -> _VersionedQuery:
        """ Gets the lastest version of a versioned timeseries of each day in a time window..
            
            Args:
                start: start timeseries for last of days. (ex. forLastOfDays("2021-03-12",...),forLastOfDays("P0Y0M-2D", ...)
                end: end timeseries for last of days. (ex. forLastOfDays("2021-03-12","2021-03-16")), forLastOfDays("P0Y0M-2D","P0Y0M2D"))
        """

        self._queryParameters.versionSelectionType = VersionSelectionType.LAST_OF_DAYS      
        if(start.startswith("P")):
            if(end is None):
                self._queryParameters.versionSelectionConfig.versionsRange.period = start
            else:
                self._queryParameters.versionSelectionConfig.versionsRange.periodFrom = start
                self._queryParameters.versionSelectionConfig.versionsRange.periodTo = end
        else:
            self._queryParameters.versionSelectionConfig.versionsRange.dateStart = start
            self._queryParameters.versionSelectionConfig.versionsRange.dateEnd = end
        return self
    def forLastOfMonths(self, start: str, end=None) -> _VersionedQuery:
        """ Gets the lastest version of a versioned timeseries of each month in a time window.
            
            Args:
                start: start timeseries for last of month. ( ex. forLastOfMonths("2021-03-12",...), forLastOfMonths("P0Y-1M0D",...) 
                end: end timeseries for last of month. (ex. forLastOfMonths("2021-03-12","2021-03-16"), forLastOfMonths("P0Y-1M0D","P0Y1M0D")) 
        """
        self._queryParameters.versionSelectionType = VersionSelectionType.LAST_OF_MONTHS
        if(start.startswith("P")):
            if(end is None):
                self._queryParameters.versionSelectionConfig.versionsRange.period = start
            else:
                self._queryParameters.versionSelectionConfig.versionsRange.periodFrom = start
                self._queryParameters.versionSelectionConfig.versionsRange.periodTo = end
        else:
            self._queryParameters.versionSelectionConfig.versionsRange.dateStart = start
            self._queryParameters.versionSelectionConfig.versionsRange.dateEnd = end
        return self
    def forLastNVersions(self, lastN: str) -> _VersionedQuery:
        """ Gets the lastest N timeseries versions that have at least a not-null value .
            
            Args:
                lastN:  ex. forLastNVersions(2)"""
        self._queryParameters.versionSelectionType = VersionSelectionType.LASTN
        self._queryParameters.versionSelectionConfig.lastN = lastN
        return self
    def forVersion(self, version) -> _VersionedQuery:
        """ Gets the specified version of a versioned timeseries.
        
            Args:
                verion: ex. forVersion("2021-03-12T14:30:00")"""
        self._queryParameters.versionSelectionType = VersionSelectionType.VERSION
        self._queryParameters.versionSelectionConfig.version = version
        return self
    def forMostRecent(self, start: str, end=None) -> _VersionedQuery:
        """ Gets the most recent version of a versioned timeseries in a time window.
        
            Args:
                start: (ex. forMostRecent("2021-03-12",...)) 
                end: (ex. forMostRecent("2021-03-12","2021-03-16")) 
        """
        self._queryParameters.versionSelectionType = VersionSelectionType.MOST_RECENT
        if(start.startswith("P")):
            if(end is None):
                self._queryParameters.versionSelectionConfig.versionsRange.period = start
            else:
                self._queryParameters.versionSelectionConfig.versionsRange.periodFrom = start
                self._queryParameters.versionSelectionConfig.versionsRange.periodTo = end
        else:
            self._queryParameters.versionSelectionConfig.versionsRange.dateStart = start
            self._queryParameters.versionSelectionConfig.versionsRange.dateEnd = end
        return self
    def withFillNull(self) -> _VersionedQuery:
        """ Optional filler strategy for the extraction.
        
            Args: 
               ex.  withFillNull() """
        self._queryParameters.fill = _NullFillStategy()
        return self
    def withFillNone(self) -> _VersionedQuery:
        """ Optional filler strategy for the extraction.
        
            Args:
                ex.  withFillNone() """
        self._queryParameters.fill = _NoFillStategy()
        return self
    def withFillLatestValue(self, period) -> _VersionedQuery:
        """ Optional filler strategy for the extraction.
        
            Args:
               ex.  withFillLatestValue("P5D") """
        self._queryParameters.fill = _FillLatestStategy(period)
        return self
    def withFillCustomValue(self, val) -> _VersionedQuery:
        """ Optional filler strategy for the extraction.
        
            Args:
                ex. 
                //Timeseries
                .withFillCustomValue(123)
         """
        self._queryParameters.fill = _FillCustomStategy(val)
        return self
    def execute(self) -> list:
        """ Execute the Query."""
        urls = self.__buildRequest()
        return super()._exec(urls)
    def executeAsync(self) -> list:
        """ Execute Async Query."""
        urls = self.__buildRequest()
        return super()._execAsync(urls)
    def __buildRequest(self):
        self.__validateQuery()
        qps = self.__partition.Partitionversioned([self._queryParameters])
        urls = []
        for qp in qps:
            url = f"/{self.__routePrefix}/{self.__buildVersionRoute()}/{self.__getGranularityPath(qp.granularity)}/{super()._buildExtractionRangeRoute(qp)}?_=1"
            if not (qp.ids is None):
                sep = ","
                ids= sep.join(map(str,qp.ids))
                enc = urllib.parse.quote_plus(ids)
                url = url + "&id=" + enc
            if not (qp.filterId is None):
                url = url + "&filterId=" + qp.filterId
            if not (qp.timezone is None):
                url = url + "&tz=" + qp.timezone
            if not (qp.transformId is None):
                url = url + "&tr=" + qp.transformId
            if not (qp.fill is None):
                url = url + "&" + qp.fill.getUrlParams()
            urls.append(url)
        return urls
    def __validateQuery(self):
        super()._validateQuery()
        if (self._queryParameters.granularity is None):
            raise Exception("Extraction granularity must be provided. Use .InGranularity() argument takes a granularity type")
        if (self._queryParameters.versionSelectionType is None):
            raise Exception("Version selection must be provided. Provide a version to query. eg .ForLastOfDays() arguments take a date range , period or period range")
    def __buildVersionRoute(self):
        switcher = {
            VersionSelectionType.LASTN: f"Last{self._queryParameters.versionSelectionConfig.lastN}",
            VersionSelectionType.MUV: f"MUV",
            VersionSelectionType.LAST_OF_DAYS: f"LastOfDays/" + self.__buildVersionRange(),
            VersionSelectionType.LAST_OF_MONTHS: f"LastOfMonths/" + self.__buildVersionRange(),
            VersionSelectionType.MOST_RECENT: f"MostRecent/" + self.__buildVersionRange(),
            VersionSelectionType.VERSION: f"Version/{self._queryParameters.versionSelectionConfig.version}"
        }
        vr = switcher.get(self._queryParameters.versionSelectionType, "VType")
        if vr == "VType" :
            raise Exception("Not supported VersionType")
        return vr
    def __buildVersionRange(self):
        vr=""
        if  (self._queryParameters.versionSelectionConfig.versionsRange.dateStart is not None) and (self._queryParameters.versionSelectionConfig.versionsRange.dateEnd is not None):
            vr = f"{self._queryParameters.versionSelectionConfig.versionsRange.dateStart}/{self._queryParameters.versionSelectionConfig.versionsRange.dateEnd}"
        elif (self._queryParameters.versionSelectionConfig.versionsRange.period is not None):
            vr = f"{self._queryParameters.versionSelectionConfig.versionsRange.period}"
        elif (self._queryParameters.versionSelectionConfig.versionsRange.periodFrom is not None) and  (self._queryParameters.versionSelectionConfig.versionsRange.periodTo is not None):
            vr = f"{self._queryParameters.versionSelectionConfig.versionsRange.dateStart}/{self._queryParameters.versionSelectionConfig.versionsRange.dateEnd}"
        return vr
    def __getGranularityPath(self,granularity):
        switcher = {
            Granularity.DAY: "Day",
            Granularity.FIFTEEN_MINUTE: "FifteenMinute",
            Granularity.HOUR: "Hour" ,
            Granularity.MINUTE: "Minute",
            Granularity.MONTH: "Month",
            Granularity.QUARTER: "Quarter",
            Granularity.TEN_MINUTE: "TenMinute",
            Granularity.THIRTY_MINUTE: "ThirtyMinute",
            Granularity.WEEK: "Week",
            Granularity.YEAR: "Year",
        }
        vr = switcher.get(granularity, "VGran")
        if vr == "VGran" :
            raise Exception("Not supported Granularity")
        return vr


class _NullFillStategy:    
    def getUrlParams(self):
        return "fillerK=Null"

class _NoFillStategy:
    def getUrlParams(self):
        return "fillerK=NoFill"

class _FillLatestStategy:
    def __init__(self, period):
        self.period = period
    def getUrlParams(self):
        return f"fillerK=LatestValidValue&fillerP={self.period}"

class _FillCustomStategy:
    def __init__(self, val):
        self.val = val
    def getUrlParams(self):
        return f"fillerK=CustomValue&fillerDV={self.val}"