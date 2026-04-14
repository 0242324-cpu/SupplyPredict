# 🚀 FASE 3 - Supabase + Render Setup

## 📦 Lo que necesitas

1. **FASE_3_EXTENDED_PROMPT.md** ← Copia esto en Claude Code (7 tareas)
2. **FASE_3_COMPLETE_GUIDE.md** ← Referencia rápida
3. **CLAUDE_CODE_TOKEN_GUIDE.md** ← Cómo usar tu token en Claude Code

---

## 🎯 QUICK START (3 pasos)

### PASO 1: Configura tu Token (En tu terminal local AHORA)
```bash
git config --global credential.helper store
cd ~/SupplyPredict
git push origin main

# Username: 0242324-cpu
# Password: [TU_TOKEN_AQUI]
```

✅ Git recordará el token automáticamente.

### PASO 2: Descarga los 2 Archivos CSV
```bash
# reorder_points.csv (1,562 registros)
curl -o ~/SupplyPredict/data/processed/reorder_points.csv \
  https://github.com/0242324-cpu/SupplyPredict/raw/main/data/processed/reorder_points.csv

# prophet_forecasts.csv (600 registros)
curl -o ~/SupplyPredict/outputs/prophet_forecasts.csv \
  https://github.com/0242324-cpu/SupplyPredict/raw/main/outputs/prophet_forecasts.csv
```

### PASO 3: Abre Claude Code y Copia el Prompt
```bash
code ~/SupplyPredict
```

Luego:
1. Abre GitHub → FASE_3_EXTENDED_PROMPT.md
2. Selecciona TODO el contenido
3. Cópialo (Cmd+C / Ctrl+C)
4. En Claude Code, pégalo en el chat
5. Presiona Enter

Claude Code te guiará a través de todas las tareas. ✅

---

## 📋 Archivos en este Repositorio

| Archivo | Propósito |
|---------|-----------|
| FASE_3_EXTENDED_PROMPT.md | ⭐ Copia esto en Claude Code (paso a paso) |
| FASE_3_COMPLETE_GUIDE.md | Referencia rápida de todos los pasos |
| CLAUDE_CODE_TOKEN_GUIDE.md | Cómo pasar tu token a Claude Code |
| FASE_3_README.md | Este archivo |

---

## ⏱️ Timeline

| Paso | Servicio | Tiempo |
|------|----------|--------|
| Configurar token | Git | 2 min |
| Descargar CSV | CLI | 1 min |
| Supabase project | Supabase | 5 min |
| SQL schema | Supabase | 2 min |
| Cargar CSV (2 archivos) | Supabase | 5 min |
| RLS policies (3 tablas) | Supabase | 5 min |
| Render Web Service | Render | 5 min |
| Crear .env | Local | 2 min |
| Verificación | Supabase | 1 min |
| **TOTAL** | - | **28 min** |

---

## 🔑 Tu Token

El token que necesitas guardar:
```
[TU_TOKEN]
```

**IMPORTANTE:**
- NO lo compartas públicamente
- NO lo comitas a GitHub
- Guárdalo en tu terminal con: `git config --global credential.helper store`
- Bórralo después de FASE 3 (revócalo en GitHub)

Ver: CLAUDE_CODE_TOKEN_GUIDE.md para más detalles.

---

## 📊 Resultado Final

Después de FASE 3, tendrás:

✅ **Supabase:**
- Proyecto creado
- 3 tablas (products, forecasts, inventory_movements)
- 1,562 productos
- 600 forecasts
- RLS policies

✅ **Render:**
- Web Service deployado
- URL de API lista
- Variables de entorno configuradas

✅ **Local:**
- Archivo .env con credenciales

---

## 🚀 Próxima Fase

**FASE 4:** FastAPI Backend (4 días - Abr 18-22)
- 4 endpoints REST
- Conexión a Supabase
- Deploy en Render

---

## ❓ Preguntas Frecuentes

**P: ¿Dónde pego el prompt?**  
R: En Claude Code, abre el chat y pega FASE_3_EXTENDED_PROMPT.md completo.

**P: ¿Cómo paso mi token a Claude Code?**  
R: Ver CLAUDE_CODE_TOKEN_GUIDE.md (3 métodos explicados).

**P: ¿Necesito pagar?**  
R: No. Supabase y Render free tiers son suficientes.

**P: ¿Cuánto tiempo toma?**  
R: 30-45 minutos si sigues los pasos.

**P: ¿Qué pasa si falla algo?**  
R: Borra el Supabase project / Render service e intenta de nuevo. Es fácil de recuperar.

---

## ✅ Checklist

Antes de empezar:
- [ ] Descargaste los 2 CSV
- [ ] Configuraste el token en tu terminal
- [ ] Tienes email para Supabase
- [ ] Tienes email para Render
- [ ] Tienes navegador listo

---

## 📞 Resumen

```
1. Terminal: git config + token setup
2. Terminal: curl descarga 2 CSV
3. Claude Code: Abre y pega FASE_3_EXTENDED_PROMPT.md
4. Sigue 7 tareas (30-45 min)
5. FASE 3 completada ✅
```

---

**Status:** ✅ Ready to deploy  
**Estimated Time:** 30-45 minutes  
**Next:** FASE 4 - FastAPI Backend

🚀 ¡Empecemos!
