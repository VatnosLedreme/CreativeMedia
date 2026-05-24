# T-101 P&ID Schematic and Guide

## T-101 P&ID ASCII Schematic

```text
                  [ Vent to Safe Area ]
                         ▲
                         │  (N2 Blanketing / Breather Valve)
                      ┌──┴──┐ PVSV-101
                      │     │
               ┌──────┴─────┴──────┐
               │    LT-101   PT-101│
               │      │        │   │
  Inlet Line   │   ┌──▼────────▼─┐ │
───────────────┼──►│             │ │
  [Line-01]    │   │  TANK T-101 │ │
 (FCV-101)     │   │             │ │
               │   │             │ │
               │   └──────┬──────┘ │
               │          │        │
               └──────────┼────────┘
                          │
                          ▼ Outlet Line [Line-02]
                        (To Pump P-101)
```

## 1. Equipment Summary: T-101 Storage Tank

*   **Tag:** T-101  
*   **Description:** Product Storage Tank  
*   **Type:** Atmospheric / Low Pressure (Vertical Cylindrical)  

## 2. Line & Piping Architecture

### Inlet Line: 3"-P-BR-01-101
*   **Source:** Process Stream upstream.
*   **Components (In Order of Flow):**
    *   Manual Isolation Valve (Gate Valve, Normally Open - **NO**).
    *   Piping Reducer (if required for instrumentation).
    *   **FE/FT-101:** Flow Element & Flow Transmitter.
    *   **FCV-101:** Flow Control Valve (Fail-Closed - **FC**).
    *   Check Valve (to prevent backflow from the tank).
    *   Tank Inlet Nozzle.

### Outlet Line: 4"-P-BR-02-101
*   **Destination:** Transfer Pump P-101 Suction.
*   **Components (In Order of Flow):**
    *   Tank Outlet Nozzle (with internal vortex breaker).
    *   Manual Isolation Valve (Gate Valve, **NO**, Car Sealed Open - **CSO**).
    *   **PI-102:** Pressure Indicator (Pump suction pressure monitoring).

### Drain & Vent Lines
*   **Drain Line (2"-D-BR-03-101):** Located at the absolute bottom. Features a Manual Gate Valve, Normally Closed (**NC**), and is plugged/capped for safety.
*   **Vent Line (2"-V-BR-04-101):** Located on the tank roof dome. Connects directly to **PVSV-101** (Pressure Vacuum Safety Valve / Breather Valve) to protect against overpressure or vacuum collapse.

## 3. Instrumentation & Control Loops

| Tag | Instrument Description | Location | Control / Safety Function |
| :--- | :--- | :--- | :--- |
| **LT-101** | Level Transmitter (Radar/Ultrasonic) | Tank Roof | Measures continuous product level. Sends signal to **LIC-101**. |
| **LIC-101** | Level Indicator Controller | DCS / Control Room | Receives signal from LT-101. Manages process logic to trigger alarms. |
| **LSHH-101** | Level Switch High-High | Tank Top | **Safety Interlock:** Automatically trips the upstream feed pump or closes FCV-101 to prevent overflow. |
| **LSLL-101** | Level Switch Low-Low | Tank Bottom | **Safety Interlock:** Trips the downstream transfer pump (P-101) to prevent dry running/cavitation. |
| **PT-101** | Pressure Transmitter | Tank Roof | Monitors internal vapor space pressure. |
| **TI-101** | Temperature Indicator | Tank Side (Thermowell) | Local gauge for manual temperature logging. |

## 4. Standard P&ID Legend for this Setup

> *   **DCS (Distributed Control System):** Indicated by a circle with a horizontal line through the center (e.g., LIC-101).
> *   **Field Mounted:** Indicated by a plain circle with no internal lines (e.g., LT-101, PT-101).
> *   **Interlock Lines:** Dashed lines representing software/electrical signaling between controllers, switches, and valves.
> *   **Process Lines:** Solid thick lines for primary fluid flow; thinner lines for vents and drains.
