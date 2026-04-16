# 🔑 Cómo Pasar tu Token a Claude Code

## ⚠️ IMPORTANTE

**NUNCA** comitas tu token a GitHub. Lo guardaremos localmente en tu terminal.

---

## 📋 Métodos para Usar el Token en Claude Code

### MÉTODO 1: Configurar Git Credentials (RECOMENDADO)

#### En tu Terminal Local (AHORA):

```bash
# 1. Configura git para recordar credenciales
git config --global credential.helper store

# 2. Haz un push (esto guardará el token)
cd ~/SupplyPredict
git push origin main

# Cuando pida credenciales:
# Username: 0242324-cpu
# Password: [TU_TOKEN_AQUI - el usuario te lo dará]

# 3. ✅ Git guardará el token en ~/.git-credentials
```

**DESPUÉS de esto:**
- Abre Claude Code
- Git usará automáticamente el token guardado
- No necesitas hacer nada más

#### En Claude Code:
```bash
# Git funcionará automáticamente
git status
git push origin main  # funcionará sin pedir contraseña
```

---

### MÉTODO 2: Variable de Entorno (Si Método 1 falla)

#### En Claude Code Terminal:

```bash
# 1. Exporta la variable (reemplaza [TOKEN] con tu token real)
export GIT_CREDENTIALS="0242324-cpu:[TU_TOKEN_AQUI]"

# 2. Configura git para usarla
git config --global credential.helper 'echo $GIT_CREDENTIALS | cut -d: -f2'

# 3. Prueba
git push origin main
```

---

### MÉTODO 3: SSH (Alternativa avanzada)

Si tienes SSH keys configuradas en GitHub:

```bash
# 1. Cambia la URL a SSH
git remote set-url origin git@github.com:0242324-cpu/SupplyPredict.git

# 2. Usa normalmente
git push origin main
```

---

## 🎯 FLUJO COMPLETO RECOMENDADO

### PASO 1: Ahora en tu Terminal Local
```bash
git config --global credential.helper store
cd ~/SupplyPredict
git push origin main

# Cuando pida:
# Username: 0242324-cpu
# Password: [TU_TOKEN]
```

### PASO 2: Abre Claude Code
```bash
code ~/SupplyPredict
```

### PASO 3: En Claude Code, verifica que git funciona
```bash
git status
git log --oneline -3
```

### PASO 4: Ahora sí, usa git libremente en Claude Code
```bash
git add .
git commit -m "tu mensaje"
git push origin main  # ¡Funcionará sin pedir token!
```

---

## ✅ Verificación

Para confirmar que el token está configurado:

```bash
# En cualquier lugar (local o Claude Code)
cat ~/.git-credentials
# Deberías ver algo como:
# https://0242324-cpu:[TOKEN]@github.com
```

---

## 🔐 SEGURIDAD

### ✅ Está BIEN:
- Token guardado en `~/.git-credentials` (archivo local)
- Token en variable de entorno (solo para esa sesión)
- Token en SSH keys (recomendado para largo plazo)

### ❌ NUNCA hagas:
- Commit del token a GitHub
- Push de `.env` con token (ya está en `.gitignore`)
- Poner token en scripts que se suban a GitHub
- Compartir tu `~/.git-credentials` con otros

---

## 🆘 Si Algo Falla

### "fatal: could not read Password"
**Solución:** Usa MÉTODO 1 en tu terminal local primero

### "Permission denied"
**Solución:** El token expiró o es inválido. Crea uno nuevo en:
https://github.com/settings/tokens

### "Authentication failed"
**Solución:** Verifica que el token tiene scope `repo`

---

## 📝 Resumen Rápido

| Situación | Solución |
|-----------|----------|
| Primer uso | MÉTODO 1: git config + push (guarda token) |
| Entorno nuevo | MÉTODO 1: repite en ese lugar |
| SSH keys listas | MÉTODO 3: usa SSH |
| Token expiró | Crea token nuevo, repite MÉTODO 1 |

---

## 🎯 Después de FASE 3

**MUY IMPORTANTE:** Cuando termines todo el desarrollo:

1. Ve a: https://github.com/settings/tokens
2. Busca tu token
3. Click **Delete**
4. Crea un token NUEVO con menos permisos si lo necesitas

Esto previene que alguien pueda usar tu token si tu sesión se compromete.

---

**Status:** Ready to use  
**Security:** Local storage, no GitHub exposure  
**Maintenance:** Delete token after development complete
