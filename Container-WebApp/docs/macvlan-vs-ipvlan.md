# macvlan vs ipvlan (Networking Comparison)

## High-Level Difference

- **macvlan** gives each container a unique virtual MAC address on the physical network.
- **ipvlan** shares the parent interface MAC and separates traffic mainly by IP.

## Comparison Table

| Criterion | macvlan | ipvlan |
| --- | --- | --- |
| Container identity on LAN | Appears as independent host with unique MAC | Appears through parent MAC with unique IP |
| Broadcast handling | More direct L2 behavior | Can reduce broadcast domain complexity |
| Host-to-container communication | Commonly blocked by default (host isolation) | Usually easier host communication depending on mode |
| Switch port MAC pressure | Higher (many container MACs) | Lower (shared parent MAC) |
| Typical use case | Need containers to look like first-class LAN devices | Need scale with lower L2 overhead |
| Complexity | Simple concept but host-isolation workaround needed | Mode-specific behavior may need deeper understanding |

## Host Isolation Note (macvlan)

In many Linux setups, the host cannot directly reach containers attached to the same macvlan network. This is expected behavior, not a bug.

Common workaround:

1. Create a macvlan sub-interface on the host.
2. Assign host-side IP in the same subnet.
3. Route traffic through that interface.

## Deployment Considerations

**macvlan** was selected for this project because:
- Meets assignment requirement for LAN-routable container IPs.
- Easy to demonstrate static IP addressing and `docker network inspect` output.
- Suitable for development and testing in virtualized environments (WSL2).

**ipvlan** would be preferable if:
- Host-to-container communication is required without workarounds.
- MAC address pressure is a concern in high-container-density environments.
- Layer-2 simplification is desired.
