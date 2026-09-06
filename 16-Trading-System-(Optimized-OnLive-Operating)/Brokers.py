# -*- coding: utf-8 -*-
"""
Created on Sat Sep  5 11:10:52 2026

@author: pabda
"""

#import libs
import threading
import time
# Own libraries
from brokers.oanda import Oanda
from brokers.fxcm import FXCM
from brokers.ib import InteractiveBrokers

#Defining class
class Brokers:
    
    """
    Class that centralizes the management of connections with the different brokers implemented in the system,
    allowing OANDA, FXCM, and Interactive Brokers interfaces to be initialized and accessed from a single control 
    point.
    """
    
    def __init__(self):
        """
        Constructor that initializes the broker connection attributes,
        setting OANDA, FXCM, and Interactive Brokers connections to None until they are established.
        """
        
        self.oanda = None
        self.fxcm = None
        self.ib = None
        
    def Oanda_Initializing(self, config_file:str) -> None:
        """
        Initializes the connection with OANDA using the provided configuration file.
        
        Parameters
        ----------
        config_file : str
            Path to the OANDA configuration file containing the credentials and
            connection settings required to access the API.
        
        Returns
        -------
        None
            The initialized OANDA API instance is stored in the class attribute.
        """
        
        # Generate connection
        oanda_api = Oanda(config_file)
        
        self.oanda = oanda_api
    
    def FXCM_Initializing(self, token: str) -> None:
        """
        Initializes the connection with FXCM using the provided API token.
        
        Parameters
        ----------
        token : str
            Authentication token required to establish a connection with the FXCM API.
        
        Returns
        -------
        None
            The initialized FXCM API instance is stored in the corresponding class attribute.
        """
        
        #Generates conection
        fxcm_api = FXCM(token=token)
        self.fxcm = fxcm_api
        
        
    def IB_Initializing(self, localhost: str = "127.0.0.1", port: int = 7497, clientId: int = 1) -> None:
        
        """
        Initializes the connection with Interactive Brokers through TWS or IB Gateway
        and starts the event processing interface in a separate thread.
        
        Parameters
        ----------
        localhost : str
            Host address used to establish the connection with TWS or IB Gateway.
            Default is "127.0.0.1".
        
        port : int
            Communication port used to connect to the Interactive Brokers API.
            Default is 7497.
        
        clientId : int
            Unique client identifier used to distinguish the API connection.
            Default is 1.
        
        Returns
        -------
        None
            The initialized Interactive Brokers API instance is stored in the
            corresponding class attribute after starting its event processing thread.
        """
        
        #Creates class instance
        ib=InteractiveBrokers()
        #creating the connection with IB TWS o IB Gateway
        ib.connect(host=localhost, port=port, clientId=clientId)
        #Initializs the thread sho excecutes the IB events interface
        api_thread = threading.Thread(target=ib.run)
        api_thread.start()
        # Wait the connection's stablishment
        time.sleep(1)
        self.ib = ib
        
# Example (Reminder)
if __name__ == "__main__":
    #Generate connection with any broker
    oanda_config_file = "brokers/credentials/config.cfg"
    
    brokers = Brokers()
    brokers.Oanda_Initializing(oanda_config_file)
    
    #Make a request for the available instruments
    print(brokers.oanda.instruments())