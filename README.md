Hospital Network Simulation

An enterprise hospital network built in Cisco Packet Tracer, simulating a segmented, redundant, and secured healthcare environment.

What I Built
VLAN segmentation across 10+ zones — clinical staff, reception, wireless, voice, management, RADIUS, and DMZ
Redundant core: EtherChannel (Po9) between two multilayer switches with active/active HSRP load-sharing
OSPF routing used end-to-end across the entire network — including all WAN/ISP-facing links (dual upstream routers, transit router, edge router) all the way through to the core switches, running as a single OSPF domain rather than BGP
Firewall as the main exit point: the ASA is the sole gateway for all outbound/inbound traffic — nothing bypasses it, so every packet leaving or entering the network is inspected and NAT'd there
DMZ: web and mail servers with static 1:1 NAT, plus a separate FTP/web service restricted to only the reception and staff VLANs
NAT hairpinning: internal VLANs reach DMZ services via their public NAT address, using the same static mappings as external clients
Wireless: WLC-managed SSIDs for staff and guest access via FlexConnect APs
VoIP: Cisco CME telephony with a dual-homed gateway for call-control redundancy
ACLs: department-level access control, enforced at the destination for reception/staff VLANs and at the source for wireless, management, and RADIUS traffic
Status

Fully built and verified end-to-end, including DMZ connectivity, NAT/hairpinning, wireless association, and VoIP redundancy.
