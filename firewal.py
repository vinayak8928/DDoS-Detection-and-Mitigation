from pox.core import core
import pox.openflow.libopenflow_01 as of
from pox.lib.revent import *
from pox.lib.util import dpidToStr
import pox.lib.packet as pkt
from pox.lib.addresses import EthAddr, IPAddr
from collections import namedtuple
import os
import csv
import codecs


log = core.getLogger()
aclSrc = "/home/demok8s/pox/pox/misc/nw_policies.csv"


class Firewall (EventMixin):

    def __init__ (self):
        self.listenTo(core.openflow)
        log.info("Starting SDN Firewall")
        self.firewall = {}


        self.FTP_PORT      = 21
        self.HTTP_PORT     = 80
        self.TELNET_PORT   = 23
        self.SMTP_PORT     = 25


    def pushRuleToSwitch (self, src, dst, ip_proto, app_proto, duration=0):
        d = int(duration)
        if d == 0:
           action = "del"
        else:
           action = "add"
        if not isinstance(d, tuple):
             d = (d,d)
        msg = of.ofp_flow_mod()
        match = of.ofp_match(dl_type = 0x800)

        # IP protocol match
        if ip_proto == "tcp":
           match.nw_proto = pkt.ipv4.TCP_PROTOCOL
        if ip_proto == "udp":
           match.nw_proto = pkt.ipv4.UDP_PROTOCOL
        elif ip_proto == "icmp":
           match.nw_proto = pkt.ipv4.ICMP_PROTOCOL
        elif ip_proto == "igmp":
           match.nw_proto = pkt.ipv4.IGMP_PROTOCOL



        # flow rule for src:host1 dst:host2
        if src != "any":
           match.nw_src = IPAddr(src)
        if dst != "any":
           match.nw_dst = IPAddr(dst)
        msg.match = match

        if action == "del":
                msg.command=of.OFPFC_DELETE
                msg.flags = of.OFPFF_SEND_FLOW_REM
                self.connection.send(msg)
        elif action == "add":
                self.connection.send(msg)


        # flow rule for src:host2 dst:host1
        if dst != "any":
           match.nw_src = IPAddr(dst)
        if src != "any":
           match.nw_dst = IPAddr(src)
        msg.match = match

        msg.idle_timeout = duration[0]
        msg.hard_timeout = duration[1]
        msg.priority = 10

    def addFirewallRule (self, src=0, dst=0, ip_proto=0, app_proto=0, duration = 0, value=True):
        if (src, dst, ip_proto, app_proto, duration) in self.firewall:
            log.warning("Rule exists: drop: src:%s dst:%s ip_proto:%s app_proto:%s duration:%s", src, dst, ip_proto, app_proto, duration)
        else:
            log.info("Rule added: drop: src:%s dst:%s ip_proto:%s app_proto:%s duration:%s", src, dst, ip_proto, app_proto, duration)
            self.firewall[(src, dst, ip_proto, app_proto, duration)]=value
            self.pushRuleToSwitch(src, dst, ip_proto, app_proto, duration)


    def delFirewallRule (self, src=0, dst=0, ip_proto=0, app_proto=0, duration = 0, value=True):
        try:
        #if (src, dst, ip_proto, app_proto) in self.firewall:
            del self.firewall[(src, dst, ip_proto, app_proto)]
            self.pushRuleToSwitch(src, dst, ip_proto, app_proto, duration)
            log.info("Rule Deleted: drop: src:%s dst:%s ip_proto:%s app_proto:%s", src, dst, ip_proto, app_proto)
        except KeyError:
            log.error("Rule doesn't exist: drop: src:%s dst:%s ip_proto:%s app_proto:%s", src, dst, ip_proto, app_proto)
        
        
    def _handle_ConnectionUp (self, event):
       
        self.connection = event.connection

        ifile  = open(aclSrc, "rb")
        reader = csv.reader(codecs.iterdecode(ifile, 'utf-8'))
        #reader = csv.reader(ifile)
        rownum = 0
        for row in reader:
            # Save header row.
            if rownum == 0:
                header = row
            else:
                colnum = 0
                for col in row:
                    #print '%-8s: %s' % (header[colnum], col)
                    colnum += 1
                self.addFirewallRule(row[1], row[2], row[3], row[4], row[5])
            rownum += 1
        ifile.close()

        log.info("Firewall rules installed on %s", dpidToStr(event.dpid))

def launch ():
    '''
    Starting the Firewall module
    '''
    core.registerNew(Firewall)


        
