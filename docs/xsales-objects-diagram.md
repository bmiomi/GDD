# Diagrama de objetos XSales (Mermaid)

```mermaid
flowchart TB
  %% Contrato base
  IPlugin["IPlugin"]
  XSalesPlugin["XSalesPlugin"]

  %% Sistema de módulos (nuevo)
  XSalesModule["XSalesModule"]
  ModuleMetadata["ModuleMetadata"]
  ModuleRegistry["ModuleRegistry"]

  %% Submódulos (migrados)
  ServerModule["ServerModule"]
  FtpModule["FtpModule"]
  StatusModule["StatusModule"]

  %% Cliente XSales
  flowchart TB
    %% Contrato base
    IPlugin["IPlugin"]
    PluginRegistry["PluginRegistry"]
    PluginContext["PluginContext"]
    XSalesPlugin["XSalesPlugin"]

    %% Sistema de módulos (nuevo)
    XSalesModule["XSalesModule"]
    ModuleMetadata["ModuleMetadata"]
    ModuleRegistry["ModuleRegistry"]

    %% Submódulos
    ServerModule["ServerModule"]
    FtpModule["FtpModule"]
    StatusModule["StatusModule"]

    %% Cliente XSales
    Xsales["Xsales"]
    XsalesLoginClient["XsalesLoginClient"]

    %% Configuración (única fuente)
    ConfigSrc["Config (src/config.py)\nconfig.yml"]
    ConfigServer["ConfigServer"]
    ConfigFtp["ConfigFtp"]
    ConfigStatus["ConfigStatus"]

    %% Flujo de plugin
    PluginRegistry --> XSalesPlugin
    XSalesPlugin -->|implements| IPlugin
    XSalesPlugin --> PluginContext
    XSalesPlugin --> ModuleRegistry

    %% Registro y ciclo de vida de submódulos
    ServerModule -->|extends| XSalesModule
    FtpModule -->|extends| XSalesModule
    StatusModule -->|extends| XSalesModule
    XSalesModule --> ModuleMetadata
    XSalesModule --> ModuleRegistry

    %% Dependencias
    ServerModule --> Xsales
    Xsales --> XsalesLoginClient

    %% Configs por módulo
    ServerModule --> ConfigServer
    FtpModule --> ConfigFtp
    StatusModule --> ConfigStatus
    ConfigServer -.-> ConfigSrc
    ConfigFtp -.-> ConfigSrc
    ConfigStatus -.-> ConfigSrc
