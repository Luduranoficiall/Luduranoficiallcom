# 🌐 Publicação e Domínio `luduranoficiall.com`

## ✅ Situação Atual
- Repositório único local: `C:\Users\User\Site Luduranoficiall`
- Git inicializado e commit criado (`feat: inicializa site profissional flask`)
- Aplicação pronta para produção (Flask + Gunicorn + Procfile)
- Repositórios antigos removidos (`Luduranoficiall-TypeScript` foi apagado)

---

## 1. Preparar repositório remoto (GitHub)
> Necessário para que a Render faça o deploy automático.

```powershell
cd "C:\Users\User\Site Luduranoficiall"
# Crie um repositório privado no GitHub chamado "luduranoficiall-site"
# Depois de criado, substitua a URL abaixo pela indicada pelo GitHub

git remote add origin https://github.com/SEU-USUARIO/luduranoficiall-site.git
git branch -M main
git push -u origin main
```

---

## 2. Deploy automático na Render
1. Acesse [https://render.com](https://render.com) e faça login (pode usar GitHub).
2. Clique em **New > Web Service**.
3. Escolha **Build and deploy from a Git repository** e selecione `luduranoficiall-site`.
4. Configure:
   - **Name**: `luduranoficiall`
   - **Region**: `Oregon` (ou a mais próxima do Brasil)
   - **Branch**: `main`
   - **Runtime**: `Python`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn app:app`
5. Clique em **Create Web Service** e aguarde o primeiro deploy (leva ~2 minutos).

> Após publicado, a Render fornecerá uma URL padrão do tipo `https://luduranoficiall.onrender.com`. Use-a temporariamente até concluir a etapa do domínio.

---

## 3. Conectar o domínio `luduranoficiall.com`
1. No painel da Render, abra o serviço e vá em **Settings > Custom Domains**.
2. Clique em **Add Custom Domain** e digite: `luduranoficiall.com`.
3. A Render mostrará dois registros DNS:
   - **Registro A** apontando para um IP (ex: `216.24.57.1`)
   - **Registro CNAME** para `www` apontando para `your-service.onrender.com`
4. No provedor onde o domínio está registrado (Registro.br, GoDaddy, etc.), crie os registros:

| Tipo | Nome host | Valor | TTL |
|------|-----------|-------|-----|
| A    | @         | IP fornecido pela Render | 300 |
| CNAME| www       | `your-service.onrender.com` | 300 |

### Se o domínio está na HostGator (ns00040.hostgator.com.br / ns00041.hostgator.com.br)

1. Acesse o **Portal do Cliente HostGator** e clique em **Entrar > Portal do Cliente**.
2. No menu lateral, abra **Domínios > Zone Editor (Editor de Zona DNS)**.
3. Escolha o domínio `luduranoficiall.com`.
4. Clique em **+ Add Record** e cadastre:
   - **Type**: `A` – **Name**: `@` – **Record**: IP que a Render mostrou – **TTL**: `300`.
   - **Type**: `CNAME` – **Name**: `www` – **Record**: `your-service.onrender.com` – **TTL**: `300`.
5. Se existirem registros A ou CNAME antigos para `@` ou `www`, remova-os para evitar conflitos.
6. Salve as alterações e aguarde a propagação (HostGator costuma levar entre 5 e 30 minutos).
7. Depois da propagação, volte na Render e clique em **Verify** para validar cada domínio.

5. Aguarde a propagação (pode levar até 30 minutos). Depois clique em **Verify** na Render.
6. Quando o status mudar para **Verified**, seu site estará acessível em `https://luduranoficiall.com` e `https://www.luduranoficiall.com`.

---

## 4. Redirecionamento e HTTPS
- Na mesma tela de domínio da Render, habilite **Force HTTPS** para garantir conexão segura.
- Ative a opção **Redirect www to apex** (ou vice-versa) para evitar conteúdo duplicado.

---

## 5. Deploy contínuo
- Toda vez que fizer `git push` para a branch `main`, a Render gerará um novo deploy automaticamente.
- Use o comando abaixo para atualizar o servidor após fazer alterações:

```powershell
git add .
git commit -m "feat: descreva a alteração"
git push
```

---

## 6. Plano de contingência
- Se o acesso precisar ser reestabelecido rapidamente antes da propagação DNS, mantenha um link temporário com o comando:

```powershell
cd "C:\Users\User\Site Luduranoficiall"
python app.py
npx localtunnel --port 5000
```

- O link gerado servirá até que `luduranoficiall.com` esteja ativo.

---

## 🧾 Checklist Final
- [x] Apagar repositórios antigos
- [x] Centralizar código no diretório `Site Luduranoficiall`
- [x] Inicializar Git e criar commit inicial
- [ ] Criar repositório no GitHub e fazer `git push`
- [ ] Criar serviço na Render e publicar
- [ ] Configurar DNS do domínio `luduranoficiall.com`
- [ ] Verificar HTTPS/redirect

Quando todos os itens estiverem marcados, o site estará oficialmente publicado em `https://luduranoficiall.com`.
