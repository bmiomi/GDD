# ============================================
# INSTRUCCIONES DE MIGRACIÓN - FASE 1
# ============================================

## ✅ Cambios Completados

### 1. Seguridad
- ✅ Creado `.env.example` con plantilla de variables de entorno
- ✅ Actualizado `.gitignore` para proteger `.env`
- ✅ Reemplazado `yaml.FullLoader` → `yaml.SafeLoader`
- ✅ Actualizado `requeriment.txt` con dependencias seguras

### 2. Arquitectura
- ✅ Creado `core/config_manager.py` - Gestor centralizado
- ✅ Modificado `plugins/xsales/confi.py` para usar ConfigManager
- ✅ Modificado `plugins/xsales/src/modules/FTP/config.py`
- ✅ Modificado `plugins/xsales/src/modules/Server/config.py`

### 3. Archivos de Configuración Limpios
- ✅ Creados archivos `.new` sin credenciales:
  - `config.yml.new`
  - `src/modules/FTP/config.yml.new`
  - `src/modules/Server/config.yml.new`

---

## 🔧 Pasos para Completar la Migración

### Paso 1: Instalar Dependencias Actualizadas
```bash
pip install -r requeriment.txt
```

### Paso 2: Crear Archivo .env con Credenciales

**Copiar template:**
```bash
cp .env.example .env
```

**Editar `.env` y completar credenciales:**
```ini
# FTP
FTP_HOST=prd1.xsalesmobile.net
FTP_PORT=990
FTP_PROTOCOL=FTPS

# Ejemplo para PRONACA
FTP_PRONACA_USER=PRONACA
FTP_PRONACA_PASS=PR0N@C@supp0rt#2018

# Server
SERVER_DEFAULT_USER=SoporteBZ
SERVER_DEFAULT_PASS=BZs2024**

# ... completar para todos los distribuidores
```

### Paso 3: Reemplazar Archivos de Configuración

**IMPORTANTE: Hacer backup primero**
```bash
# Backup
cp plugins/xsales/config.yml plugins/xsales/config.yml.backup
cp plugins/xsales/src/modules/FTP/config.yml plugins/xsales/src/modules/FTP/config.yml.backup
cp plugins/xsales/src/modules/Server/config.yml plugins/xsales/src/modules/Server/config.yml.backup

# Reemplazar con versiones limpias
mv plugins/xsales/config.yml.new plugins/xsales/config.yml
mv plugins/xsales/src/modules/FTP/config.yml.new plugins/xsales/src/modules/FTP/config.yml
mv plugins/xsales/src/modules/Server/config.yml.new plugins/xsales/src/modules/Server/config.yml
```

### Paso 4: Verificar Funcionamiento

**Probar que la aplicación carga correctamente:**
```bash
python main.py
```

**Si hay errores:**
1. Verificar que `.env` esté completo
2. Revisar logs de error
3. Validar variables de entorno requeridas

---

## 🔐 Verificación de Seguridad

### ✅ Checklist
- [ ] Archivo `.env` creado y NO está en Git
- [ ] `.env.example` sí está en Git (sin credenciales)
- [ ] `.gitignore` incluye `.env`
- [ ] Archivos `config.yml` limpios (sin credenciales)
- [ ] Código usa `config_manager` para credenciales
- [ ] `yaml.SafeLoader` en uso (no FullLoader)
- [ ] Dependencias actualizadas

---

## 📝 Notas Importantes

### Migración Gradual
El código actual tiene **fallback a config.yml** si no encuentra variables en `.env`.
Esto permite migración gradual:

1. **Primera ejecución**: Usa credenciales de config.yml (legacy)
2. **Vas agregando** credenciales a `.env`
3. **Eventualmente** puedes eliminar todas las credenciales de config.yml

### Beneficios Logrados

✅ **Seguridad**: Credenciales fuera del código versionado
✅ **Flexibilidad**: Diferentes credenciales por entorno (dev/prod)
✅ **Mantenibilidad**: ConfigManager centralizado
✅ **Actualizaciones**: Dependencias seguras

### Próximos Pasos (Fase 2)

Una vez que confirmes que todo funciona:
- Refactorizar arquitectura de plugins
- Separar queries SQL en archivos dedicados
- Mejorar manejo de errores

---

## 🆘 Troubleshooting

**Error: "Variable de entorno no encontrada"**
```
Solución: Agregar variable faltante en .env
```

**Error: "yaml.constructor.ConstructorError"**
```
Solución: Verificar que no haya sintaxis Python en config.yml
```

**Error al cargar config.yml**
```
Solución: Verificar sintaxis YAML con yamllint
```

---

## 📞 Contacto

Si encuentras problemas, revisa:
1. Logs de error completos
2. Variables de entorno definidas
3. Sintaxis de archivos YAML
