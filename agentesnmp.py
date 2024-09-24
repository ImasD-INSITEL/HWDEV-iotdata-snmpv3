
from pysnmp.hlapi import *
from datetime import datetime
from pysnmp import debug
from pysnmp.carrier.asyncore.dgram import udp
from pysnmp.entity import engine, config
from pysnmp.entity.rfc3413 import cmdrsp, context
from pysnmp.proto.api import v2c
from pysnmp.smi import builder, instrum, exval, error, view
from pysnmp.proto import rfc1902
import threading



snmpEngine = engine.SnmpEngine()

# Transport setup
# UDP over IPv4 and allow any IP address at port 161
config.addTransport(
    snmpEngine,
    udp.domainName,
    udp.UdpTransport().openServerMode(('10.10.135.7', 16161))      #snmpget -v3 -u admin -l authPriv -a MD5 -A admin1234 -x DES -X admin1234 10.10.135.7:16161 1.3.6.1.4.1.6263.1.2   // snmpwalk -v 3 -u admin -a MD5 -A admin1234 -x des -X admin1234 -l authPriv -L n -m all 10.10.135.7:16161 1
)



# SNMPv3/USM setup
# user: usr-sha-des, auth: SHA, priv AES128
config.addVacmUser(snmpEngine, 3, 'santi', 'authPriv', (1, 3, 6, 1, 4, 1, 6263, 1, 2),(1, 3, 6, 1, 4, 1, 6263, 1, 1))
config.addVacmUser(snmpEngine, 3, 'santi', 'authPriv', (1, 3, 6, 1, 4),(1, 3, 6, 1, 4, 1, 6263,1),(1, 3, 6, 1, 4, 1, 6263))

config.addV3User(
    snmpEngine, 'santi',
    config.usmHMACMD5AuthProtocol, 'admin1234',#    config.usmHMACSHAAuthProtocol, 'admin1234',
    config.usmDESPrivProtocol, 'admin1234'#config.usmAesCfb128Protocol, 'admin1234'
)

# Limit readonly access to just the MIBs used here at VACM for the v3 user.  Widen if need be.

# Create an SNMP context
snmpContext = context.SnmpContext(snmpEngine)

mibBuilder = snmpContext.getMibInstrum().getMibBuilder()
(MibTable,
 MibTableRow,
 MibTableColumn,
 MibScalarInstance) = mibBuilder.importSymbols(
    'SNMPv2-SMI',
    'MibTable',
    'MibTableRow',
    'MibTableColumn',
    'MibScalarInstance'
)
mibBuilder.exportSymbols(
    'MY-MIB',
    ifTable=MibTable((1, 3, 6, 1, 4, 6263), ).setMaxAccess('readcreate'),
    ifEntry=MibTableRow((1, 3, 6, 1, 4, 1, 6263, 1)).setMaxAccess('readcreate').setIndexNames((0, 'MY-MIB', 'ifIndex')),
    ifIndex=MibTableColumn((1, 3, 6, 1, 4, 1, 6263, 1, 1), v2c.Integer32()).setMaxAccess('readcreate'),
    ifVoltaje=MibTableColumn((1, 3, 6, 1, 4, 1, 6263, 1, 3), v2c.Integer32()).setMaxAccess('readcreate'),
    ifDescr=MibTableColumn((1, 3, 6, 1, 4, 1, 6263, 1, 2), v2c.OctetString()).setMaxAccess('readcreate'),
    ifTem=MibTableColumn((1, 3, 6, 1, 4, 1, 6263, 1, 4), v2c.OctetString()).setMaxAccess('readcreate'),
    ifHum=MibTableColumn((1, 3, 6, 1, 4, 1, 6263, 1, 5), v2c.OctetString()).setMaxAccess('readcreate'),
    ifAcVoltaje=MibTableColumn((1, 3, 6, 1, 4, 1, 6263, 1, 6), v2c.OctetString()).setMaxAccess('readcreate'),
    ifDcVoltaje=MibTableColumn((1, 3, 6, 1, 4, 1, 6263, 1, 7), v2c.OctetString()).setMaxAccess('readcreate')

)
# mibBuilder.exportSymbols(
#     'MY-MIB',
#     ifTable=MibTable((1, 3, 6, 1, 4, 1, 20408, 3, 1, 1, 1, 4), ).setMaxAccess('readcreate'),
#     ifEntry=MibTableRow((1, 3, 6, 1, 4, 1, 20408, 3, 1, 1, 1, 4 , 1)).setMaxAccess('readcreate').setIndexNames((0, 'MY-MIB', 'ifIndex')),
#     ifIndex=MibTableColumn((1, 3, 6, 1, 4, 1, 20408, 3, 1, 1, 1, 4, 1, 1), v2c.Integer32()).setMaxAccess('readcreate'),
#     ifDescr=MibTableColumn((1, 3, 6, 1, 4, 1, 20408, 3, 1, 1, 1, 4, 1, 2), v2c.OctetString()).setMaxAccess('readcreate')
# )


# All WiFi products use the ifIndex of 1 for the WLAN interface.

#snmpget -v3 -u santi -l authPriv -a MD5 -A admin1234 -x DES -X admin1234 10.10.135.7:16161 1.3.6.1.4.1.6263.1.1.1
(ifEntry,
 ifIndex,
 ifVoltaje,
 ifDescr,
 ifTem,
 ifHum,
 ifAcVoltaje,
 ifDcVoltaje
 ) = mibBuilder.importSymbols(
    'MY-MIB',
    'ifEntry',
    'ifIndex',
    'ifVoltaje',
    'ifDescr',
    'ifTem',
    'ifHum',
    'ifAcVoltaje',
    'ifDcVoltaje'
)


rowInstanceId = (1,)
mibInstrumentation = snmpContext.getMibInstrum()
mibInstrumentation.writeVars(
    ((ifIndex.name + rowInstanceId, 1),
     (ifVoltaje.name + rowInstanceId, 10),
     (ifDescr.name + rowInstanceId, 'Trnsmision agente Raspberry: Full conect'),
     (ifTem.name + rowInstanceId, 'Trnsmision agente Raspberry: Full conect'),
     (ifHum.name + rowInstanceId, 'Trnsmision agente Raspberry: Full conect'),
     (ifAcVoltaje.name + rowInstanceId, 'Trnsmision agente Raspberry: Full conect'),
     (ifDcVoltaje.name + rowInstanceId, 'Trnsmision agente Raspberry: Full conect')
     )

)
counter = 10

def update_variables():
    global counter
    counter += 1
    mibInstrumentation.writeVars(
        ((ifVoltaje.name + rowInstanceId, counter),
         (ifTem.name + rowInstanceId, str(counter)),
         (ifHum.name + rowInstanceId, str(counter)),
         (ifAcVoltaje.name + rowInstanceId, str(counter)),
         (ifDcVoltaje.name + rowInstanceId, str(counter))
         )
    )
    varBinds = [((1, 3, 6, 1, 4, 1, 6263, 1, 2, 1), None)]
    result = mibInstrumentation.readVars(varBinds)
    ##variable=mibInstrumentation.readVars(ifDescr.name + rowInstanceId)
    print(result[0][1])
    # Call this function again after 1 second
    threading.Timer(10, update_variables).start()
    print(counter)
update_variables()


# Register SNMP Applications at the SNMP engine for particular SNMP context
cmdrsp.GetCommandResponder(snmpEngine, snmpContext)
cmdrsp.SetCommandResponder(snmpEngine, snmpContext)
cmdrsp.NextCommandResponder(snmpEngine, snmpContext)
cmdrsp.BulkCommandResponder(snmpEngine, snmpContext)

# Register an imaginary never-ending job to keep I/O dispatcher running forever
snmpEngine.transportDispatcher.jobStarted(1)

# Run I/O dispatcher which would receive queries and send responses
try:
    snmpEngine.transportDispatcher.runDispatcher()
except:
    snmpEngine.transportDispatcher.closeDispatcher()
    raise