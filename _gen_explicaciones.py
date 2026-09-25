# Generates capitulos/_explicaciones/*.md — one collapsible lightbulb
# callout per technical term, included in chapters via {{< include >}}.
import os, textwrap

OUT = "capitulos/_explicaciones"

# slug -> (term shown in title, beginner-friendly body in Spanish)
EXPLAIN = {
"api": ("API", """
Una **API** (Application Programming Interface) es el menú de un
programa: la lista de operaciones que otros programas pueden pedirle.
Tu frontend no habla con la base de datos — le pide cosas a la API,
y la API decide.
"""),
"endpoint": ("endpoint", """
Un **endpoint** es una puerta específica de una API: la combinación de
verbo + dirección, como `GET /tasks` (dame la lista) o `POST /tasks`
(crea una). Una API es el restaurante; cada endpoint es un plato del
menú.
"""),
"json": ("JSON", """
**JSON** (JavaScript Object Notation) es el formato universal para
mover datos entre programas: texto con llaves y corchetes,
`{"title": "Comprar leche", "done": false}`. Casi cualquier lenguaje
lo lee y lo escribe.
"""),
"request": ("request / petición", """
Un **request** (petición) es el mensaje que un cliente le manda al
servidor: "quiero X". Tiene una dirección (URL), un verbo (GET, POST…),
headers (metadatos) y a veces un body (los datos). La respuesta es el
**response**.
"""),
"cliente": ("cliente", """
El **cliente** es quien *pide*: el navegador, una app móvil, otro
servidor. El **servidor** es quien *atiende* y responde. La misma
computadora puede ser cliente de una cosa y servidor de otra.
"""),
"servidor": ("servidor", """
Un **servidor** es una computadora que espera peticiones y las responde
24/7. Físicamente no es nada mágico: es una máquina (a veces una VM
alquilada) corriendo tu programa, con la diferencia de que está siempre
encendida y conectada.
"""),
"puerto": ("puerto", """
Un **puerto** es una puerta numerada dentro de una computadora: la IP
llega al edificio, el puerto al departamento. `:3000` = "la app que
escucha en el departamento 3000". Postgres suele usar 5432, HTTP el 80,
HTTPS el 443.
"""),
"localhost": ("localhost / 127.0.0.1", """
**localhost** significa "esta misma máquina" — es la dirección que tu
computadora usa para hablarse a sí misma. Cuando desarrollas, el
"servidor" y el "cliente" viven en tu laptop: por eso todo es
`localhost:3000`.
"""),
"proceso": ("proceso", """
Un **proceso** es un programa en ejecución: el sistema operativo le da
memoria propia y un lugar en la fila del CPU. Tu API es un proceso;
Postgres es otro; el navegador es varios. Que "se caiga el proceso"
= el programa murió.
"""),
"memoria": ("memoria (RAM)", """
La **memoria RAM** es el escritorio de trabajo del programa: rápida,
pero se borra al apagar. Los datos que deben sobrevivir van a disco o a
la base de datos. Por eso `let tasks = []` pierde todo al reiniciar.
"""),
"cpu": ("CPU / núcleos", """
El **CPU** es el cerebro que ejecuta instrucciones; cada **núcleo**
puede ejecutar una cosa a la vez (por eso importan la concurrencia y
los procesos paralelos). "CPU-bound" = el límite es el cálculo, no la
espera.
"""),
"runtime": ("runtime", """
El **runtime** es el motor que ejecuta tu código: Node.js es el runtime
de JavaScript fuera del navegador; CPython es el de Python; Go compila
a binario y el runtime va empaquetado dentro. Es "quien corre" lo que
escribiste.
"""),
"entorno": ("entorno (environment)", """
Un **entorno** es una instancia completa donde corre tu app con su
propia config y datos: *local* (tu máquina), *staging* (réplica de
prueba), *producción* (la real). Cada entorno tiene sus propias llaves
y su propia base de datos.
"""),
"produccion": ("producción", """
**Producción** (prod) es el entorno real: donde están los usuarios, los
datos que importan y las consecuencias. Todo lo demás — local, staging —
existe para que los errores ocurran antes de llegar ahí.
"""),
"staging": ("staging", """
**Staging** es el ensayo general: una copia de producción (misma
config, datos falsos o anonimizados) donde pruebas el deploy antes de
hacerlo de verdad. Si falla ahí, falló gratis.
"""),
"terminal": ("terminal / consola", """
La **terminal** (consola, línea de comandos) es la interfaz de texto con
el sistema operativo: escribes comandos, lees resultados. Es como
hablarle a la computadora por cartas en vez de señalar con el mouse.
"""),
"cli": ("CLI", """
Un **CLI** (Command Line Interface) es un programa que se usa escribiendo
comandos en la terminal: `git`, `npm`, `docker` son CLIs. Lo contrario
es una GUI (interfaz gráfica con botones).
"""),
"path": ("PATH", """
**PATH** es la lista de carpetas donde la terminal busca programas
cuando escribes un comando. Si `node` no está en el PATH, la terminal
responde "command not found" aunque esté instalado en algún lado.
"""),
"git": ("Git", """
**Git** es el historial de tu proyecto: cada *commit* es una foto del
código con mensaje. Permite volver atrás, trabajar en ramas paralelas
y fusionar el trabajo de varias personas sin pisarse.
"""),
"repositorio": ("repositorio", """
Un **repositorio** (repo) es la carpeta del proyecto con todo su
historial Git adentro. GitHub/GitLab son servicios que hospedan repos
para compartirlos y respaldarlos.
"""),
"commit": ("commit", """
Un **commit** es una foto guardada del código con un mensaje que dice
por qué cambió. La historia del proyecto es una cadena de commits:
puedes volver a cualquiera, ver qué cambió y quién lo hizo.
"""),
"pull-request": ("pull request (PR) / merge", """
Un **pull request** es pedir que tus cambios entren a la rama
principal: otros los revisan, comentan y aprueban antes del *merge*
(fusión). Es la puerta de calidad del trabajo en equipo.
"""),
"code-review": ("code review", """
Un **code review** es un colega leyendo tu cambio antes de que entre:
busca bugs, malas decisiones y estilo. Suena a examen, pero es donde
más se aprende — los seniors aprenden leyendo, no escribiendo.
"""),
"framework": ("framework", """
Un **framework** es un esqueleto de aplicación ya decidido: te da la
estructura (rutas, validación, errores) y tú llenas la lógica.
Diferencia con librería: la librería la llamas tú; el framework te
llama a ti.
"""),
"dependencia": ("dependencia", """
Una **dependencia** es código de terceros que tu proyecto usa:
`npm install`, `pip install`, `go get` las traen. Cada una es deuda —
ahora funciona, pero hay que mantenerla, actualizarla y confiar en ella.
"""),
"paquete": ("paquete / package manager", """
Un **paquete** es una librería empaquetada lista para instalar. El
*package manager* (npm, pip, go mod) las descarga, resuelve versiones
compatibles y las registra en `package.json` / `pyproject.toml` /
`go.mod`.
"""),
"modulo": ("módulo / import", """
Un **módulo** es un archivo de código que exporta cosas para que otros
archivos las importen. Es la unidad de organización: en vez de un
archivo gigante, el código vive en módulos con responsabilidad propia.
"""),
"build": ("build", """
El **build** (construcción) es el proceso que convierte tu código
fuente en algo ejecutable/entregable: compilar TypeScript a JS,
empaquetar el frontend, armar la imagen Docker. Lo que se despliega es
el resultado del build, no tu código crudo.
"""),
"compilador": ("compilador / transpilador", """
Un **compilador** traduce código a otra forma: TypeScript → JavaScript
(transpila), Go → binario (compila). Atrapa errores antes de ejecutar.
`tsc`, `esbuild`, `go build` son compiladores.
"""),
"tipado": ("tipos / tipado estático", """
Los **tipos** (`int`, `string`, `boolean`, `Task`) son el contrato de
cada dato. *Tipado estático* (TypeScript, Go, Python con hints) = los
tipos se revisan al escribir, no cuando explota en producción.
"""),
"serializar": ("serializar / parse", """
**Serializar** es convertir un objeto en memoria a texto viajero
(`JSON.stringify`); **parsear/deserializar** es el viaje de vuelta
(`JSON.parse`). Todo lo que cruza la red o la BD pasa por este par.
"""),
"async-await": ("async / await / Promise", """
**Async/await** es la sintaxis para operaciones que tardan (red, disco):
`await` pausa *esa función* sin congelar el programa entero. Una
`Promise` es la "promesa" de un resultado futuro — el ticket que
recibes mientras lo preparan.
"""),
"hilo": ("hilo / thread / goroutine", """
Un **hilo** (thread) es una línea de ejecución dentro del proceso:
varios hilos = varias cosas "a la vez". Go los hace baratísimos
(goroutines); Node usa un solo hilo con event loop; Python tiene el
GIL que los limita.
"""),
"concurrencia": ("concurrencia vs paralelismo", """
**Concurrencia** = manejar muchas cosas en progreso (atender 1000
requests intercalando). **Paralelismo** = ejecutar varias a la vez en
varios núcleos. Un camarero con 10 mesas es concurrente; 10 camareros
son paralelos.
"""),
"event-loop": ("event loop", """
El **event loop** es el mecanismo de Node: un solo hilo que toma tareas
de una cola sin parar. Mientras una tarea espera (BD, red), atiende
otra. Por eso Node escala en I/O con un solo hilo — nunca se sienta a
esperar.
"""),
"gil": ("GIL", """
El **GIL** (Global Interpreter Lock) es el candado de Python: solo un
hilo ejecuta Python a la vez por proceso. Por eso Python escala con
*procesos* (workers) y `asyncio`, no con hilos de CPU.
"""),
"stdout": ("stdout / stderr", """
**stdout** es la salida normal de un programa (lo que imprime);
**stderr** es la salida de errores. En Docker y systemd los logs son
stdout capturado — por eso "loggea a consola" es la práctica correcta.
"""),
"base-de-datos": ("base de datos", """
Una **base de datos** es el programa que guarda datos de forma
permanente y los responde rápido. Relacional (Postgres): tablas con
relaciones. No relacional: documentos, clave-valor, grafos — cada una
para una forma de dato distinta.
"""),
"query": ("query / consulta", """
Una **query** es la pregunta que le haces a la base de datos en SQL:
`SELECT * FROM tasks WHERE done = false`. La BD traduce la pregunta a
un plan de búsqueda — por eso los índices importan.
"""),
"esquema": ("esquema (schema)", """
El **esquema** es el plano de la base de datos: qué tablas hay, qué
columnas tiene cada una y de qué tipo. Es contrato: una fila que no
cumple el esquema no entra. Se cambia con migraciones, no a mano.
"""),
"indice": ("índice (index)", """
Un **índice** es la tabla de contenido de una tabla: sin él, buscar un
usuario es leer las 10 millones de filas (*seq scan*); con él, es ir
directo a la página. Se crea según cómo se consulta, y cada uno cuesta
escrituras.
"""),
"migracion": ("migración", """
Una **migración** es un cambio versionado del esquema: un archivo que
dice "crea esta columna" (up) y "bórrala" (down). Son el historial Git
de la estructura de la BD — se aplican en orden y no se editan una vez
aplicadas.
"""),
"transaccion": ("transacción", """
Una **transacción** es un grupo de operaciones que se confirman juntas
o no se confirma ninguna: transferir dinero = restar de A *y* sumar a
B. Si falla a la mitad sin transacción, el dinero desapareció.
"""),
"pool": ("pool de conexiones", """
Un **pool** es el staff de conexiones a la BD: abrir una conexión por
request es caro, así que el pool mantiene ~10–20 abiertas y las presta.
El request la usa, la devuelve, y la siguiente la reutiliza.
"""),
"orm": ("ORM", """
Un **ORM** (Object-Relational Mapper) traduce entre objetos del código
y filas de la tabla: `task.save()` en vez de `INSERT`. Cómodo para el
CRUD, peligroso si no sabes qué SQL genera (el N+1 nace ahí).
"""),
"join": ("JOIN", """
Un **JOIN** combina tablas por su relación: "cada tarea con el nombre
de su proyecto". Es la superpotencia relacional — en una query traes
lo que en NoSQL serían varios viajes.
"""),
"foreign-key": ("foreign key / clave foránea", """
Una **foreign key** es un puntero verificado: `tasks.project_id`
apunta a `projects.id` y la BD *garantiza* que el proyecto existe.
Es la diferencia entre "el dato dice 5" y "el dato apunta a algo real".
"""),
"lock": ("lock / bloqueo (FOR UPDATE)", """
Un **lock** de fila (`SELECT ... FOR UPDATE`) dice "esta fila es mía
hasta que mi transacción termine": otros que la pidan esperan. Es como
el candado del probador de ropa — evita que dos editen lo mismo.
"""),
"snapshot": ("snapshot", """
Un **snapshot** es una foto completa del estado en un momento: el
documento entero en la revisión 14. Restaurar = leer la foto, no
reconstruir sumando cambios. Cuesta más disco; regala simplicidad.
"""),
"diff": ("diff", """
Un **diff** es la lista de diferencias entre dos versiones: "línea 3
cambió de A a B". Git lo usa para mostrar cambios; los docs
colaborativos para transmitir ediciones sin mandar todo el documento.
"""),
"constraint": ("constraint / restricción", """
Una **constraint** es una regla que la BD hace cumplir: `NOT NULL`,
`UNIQUE`, `CHECK (price > 0)`, `FOREIGN KEY`. Es la última línea de
defensa — el código puede tener bugs; la constraint no perdona.
"""),
"inyeccion-sql": ("inyección SQL", """
La **inyección SQL** es el clásico de romper la query: si concatenas
input del usuario en el SQL, el usuario *escribe SQL*. `' OR 1=1--`
borra tablas. La vacuna: queries parametrizadas (`$1`), siempre.
"""),
"n-mas-1": ("N+1", """
El **N+1** es el bug de rendimiento más común: 1 query para la lista +
N queries (una por ítem) para los detalles = 101 viajes para 100
tareas. Se cura con JOIN o agregación: una sola query que lo trae todo.
"""),
"paginacion": ("paginación", """
**Paginar** es servir la lista en páginas (20 por 20) en vez de las
10 millones. `LIMIT 21` + cursor = la página siguiente se pide con la
última fila vista, no con "salta 40000" (offset, que se degrada).
"""),
"crud": ("CRUD", """
**CRUD** = Create, Read, Update, Delete — las cuatro operaciones
básicas sobre un recurso. `POST/GET/PUT/DELETE /tasks`. El 80% de las
APIs del mundo es CRUD bien hecho sobre varias tablas.
"""),
"openapi": ("OpenAPI", """
**OpenAPI** es el formato estándar para describir una API: cada
endpoint, sus parámetros, sus respuestas, sus errores. De ese archivo
salen la documentación, los clientes generados y los tests de contrato.
"""),
"adr": ("ADR", """
Un **ADR** (Architecture Decision Record) es una nota corta que dice:
contexto, qué decidimos, qué alternativas descartamos y qué precio
pagamos. En 6 meses el código dice *qué*; el ADR recuerda *por qué*.
"""),
"regex": ("regex / expresión regular", """
Una **regex** es un patrón de búsqueda en texto: `^\d+$` = "solo
dígitos". Poderosa y críptica — úsala para validar formatos, no para
parsear cosas complejas.
"""),
"autenticacion": ("autenticación", """
La **autenticación** responde "¿quién eres?" — login, contraseña,
token. Se confunde con autorización ("¿qué puedes hacer?"), que es la
pregunta siguiente. Primero te identificas, luego te dejan o no pasar.
"""),
"autorizacion": ("autorización / permisos", """
La **autorización** responde "¿qué puedes hacer?": eres usuario válido
(autenticado), pero ¿puedes borrar *esta* tarea? Se decide por rol o
por ownership — y se verifica en cada request, no se recuerda.
"""),
"sesion": ("sesión", """
Una **sesión** es la conversación continuada entre tú y el servidor:
HTTP no recuerda nada entre requests, así que la sesión (vía cookie o
token) es el "pulso de mano" que te identifica en cada llamada.
"""),
"cookie": ("cookie", """
Una **cookie** es un dato que el servidor pone en tu navegador y el
navegador devuelve en cada request. `httpOnly` = JavaScript no puede
leerla (el XSS no la roba); `Secure` = solo viaja por HTTPS.
"""),
"token": ("token", """
Un **token** es una credencial portable: una cadena que dice quién eres
y hasta cuándo. El servidor la emite tras el login; el cliente la
presenta en cada request en vez de la contraseña.
"""),
"jwt": ("JWT", """
Un **JWT** (JSON Web Token) es un token *firmado*: el servidor lo
genera con su secreto y puede verificarlo sin consultar la BD. Ojo:
está firmado, no cifrado — cualquiera puede leer su contenido, pero no
modificarlo.
"""),
"hash": ("hash / bcrypt", """
Un **hash** es una función de un solo sentido: `contraseña →
`$2b$10$...`. No se puede revertir — por eso las contraseñas se
*hashean*, no se *cifran*. bcrypt es lento a propósito: fuerza bruta
cara para el atacante.
"""),
"cifrado": ("cifrado / encriptación", """
El **cifrado** convierte datos en basura legible solo con la llave —
y a diferencia del hash, *se puede revertir*. HTTPS cifra el cable; las
contraseñas NO se cifran, se hashean (no hay por qué revertirlas).
"""),
"firma": ("firma / HMAC", """
Una **firma** (HMAC) prueba que un mensaje es auténtico y no fue
tocado: se calcula con un secreto sobre el contenido. Los webhooks la
usan para que verifiques "esto realmente vino de Stripe".
"""),
"roles": ("roles / RBAC", """
Los **roles** agrupan permisos: *viewer* lee, *editor* escribe, *admin*
gestiona. RBAC = el permiso depende del rol que tienes *en ese
recurso* — puedes ser admin de un equipo y viewer de otro.
"""),
"cors": ("CORS", """
**CORS** es la política del navegador: por defecto, una página de
`sitioA.com` no puede leer respuestas de `apiB.com`. El servidor
declara qué orígenes acepta. Es protección del navegador, no del
servidor (curl ni la ve).
"""),
"xss": ("XSS / CSRF", """
**XSS**: un atacante inyecta JavaScript en tu página (roba datos,
localStorage). **CSRF**: un sitio malicioso hace que tu navegador
dispare requests con tus cookies. Los fixes: sanitizar, httpOnly,
SameSite.
"""),
"rate-limit": ("rate limit / 429", """
El **rate limit** es un presupuesto de requests: "5 logins por minuto
por IP". Quien lo excede recibe `429 Too Many Requests`. Frena fuerza
bruta, bugs de loop infinito y abuso.
"""),
"owasp": ("OWASP", """
**OWASP** es la organización que publica las listas de vulnerabilidades
más reales — el *API Security Top 10* es la checklist de lo que
efectivamente rompe las APIs: auth rota, BOLA, inyección…
"""),
"middleware": ("middleware", """
Un **middleware** es un filtro en la cadena del request: pasa por él
antes de llegar a tu handler. Auth es middleware — "verifica el token"
vive una vez y protege todas las rutas, no se copia en cada una.
"""),
"log": ("log / logging estructurado", """
Un **log** es el diario del programa: qué pasó, cuándo, con qué
request. *Estructurado* = en JSON con campos (`request_id`, `user_id`),
para filtrar por máquina y no con los ojos.
"""),
"variable-de-entorno": ("variable de entorno", """
Una **variable de entorno** es configuración que vive fuera del código:
`DATABASE_URL`, `JWT_SECRET`. El mismo binario corre en dev y prod
con distintas vars — los secretos nunca se escriben en el código.
"""),
"secreto": ("secreto", """
Un **secreto** es un dato que no puede publicarse: contraseñas de BD,
llaves de API, el secreto que firma los JWT. Viven en `.env` (fuera de
git) o en un secret manager — nunca en el código ni en el repo.
"""),
"secret-manager": ("secret manager", """
Un **secret manager** (AWS Secrets Manager, Azure Key Vault) es la
caja fuerte de la nube: guarda secretos cifrados, los rota, registra
quién los leyó. La app los pide al arrancar en vez de tenerlos en
archivos.
"""),
"deploy": ("deploy / despliegue", """
Un **deploy** es poner tu código a correr en el servidor: copiar la
imagen, iniciar el proceso, verificar que responde. El objetivo es que
sea aburrido — automático, repetible, con rollback.
"""),
"dns": ("DNS", """
El **DNS** es la agenda telefónica de internet: traduce
`nexus.com` → `203.0.113.10`. Tu dominio apunta vía DNS a tu
load balancer o servidor — por eso "propagación de DNS" toma minutos.
"""),
"dominio": ("dominio", """
Un **dominio** es el nombre que compras (midominio.com) y apuntas a tu
servidor por DNS. Sin él, tus usuarios tendrían que memorizar una IP.
El HTTPS serio requiere dominio.
"""),
"ip": ("dirección IP", """
Una **IP** es la dirección numérica de una máquina en la red:
`203.0.113.10`. Los servidores tienen IP pública; dentro de una VPC
tienen IPs privadas que internet no ve.
"""),
"tls": ("HTTPS / TLS / certificado", """
**HTTPS** = HTTP viajando cifrado por **TLS**: nadie en el camino puede
leer ni alterar el tráfico. El **certificado** es la credencial que
prueba que el servidor es quien dice — lo emite una autoridad y hay que
renovarlo.
"""),
"proxy": ("reverse proxy", """
Un **reverse proxy** (nginx, ALB, Cloudflare) es el portero: recibe
todo el tráfico en el 443, termina TLS y reparte a tu app interna.
La app nunca mira a internet directamente — el proxy la protege.
"""),
"cdn": ("CDN", """
Una **CDN** (Content Delivery Network) es una red de copias: tu
estático se cachea en servidores cercanos al usuario. El de Buenos
Aires no viaja a Virginia por una imagen — la recibe del nodo local.
"""),
"cache": ("caché / Redis", """
Un **caché** es una copia rápida de algo costoso de obtener: el
resultado de una query pesada, la sesión. Redis es el caché estándar.
La regla de oro: cachear es fácil, *invalidar* (saber cuándo el caché
ya no vale) es lo difícil.
"""),
"docker": ("Docker", """
**Docker** empaqueta tu app con todo lo que necesita (runtime,
librerías, config) en una **imagen** — el mismo paquete corre idéntico
en tu laptop y en producción. Es la respuesta a "en mi máquina sí
funcionaba".
"""),
"contenedor": ("contenedor", """
Un **contenedor** es un proceso con mochila propia: corre aislado con
su filesystem y sus librerías, pero comparte el kernel de la máquina —
por eso arranca en milisegundos donde una VM tarda minutos.
"""),
"imagen": ("imagen (Docker)", """
Una **imagen** es la plantilla inmutable de la que nacen contenedores:
la foto del disco + cómo arrancar. Se construye en capas (Dockerfile),
se versiona con tags, se publica en un registry.
"""),
"volumen": ("volumen (Docker)", """
Un **volumen** es almacenamiento que sobrevive al contenedor: el
contenedor muere y renace, el volumen (los datos de Postgres) sigue
ahí. Sin volumen, `docker compose down` borra tu base de datos.
"""),
"compose": ("Docker Compose", """
**Docker Compose** describe un sistema de varios contenedores en un
YAML: la app + Postgres + Redis, sus redes y volúmenes. `docker
compose up` levanta el entorno completo de desarrollo con un comando.
"""),
"registry": ("registry (Docker)", """
Un **registry** es el almacén de imágenes (Docker Hub, ECR, Artifact
Registry): el CI empuja `nexus:v42`, el servidor la jala. Es el
intermediario entre "se construyó" y "está corriendo".
"""),
"multi-stage": ("multi-stage build", """
Un **multi-stage build** compila la imagen en dos fases: una gorda con
todo el toolchain (compila), una flaca que solo recibe el resultado
(corre). La imagen final es chica y sin compiladores ni dev-deps.
"""),
"cicd": ("CI/CD / pipeline", """
**CI** (integración continua): cada push corre tests y build
automático. **CD** (despliegue continuo): si todo pasa, se despliega
solo. El **pipeline** es la cadena de pasos — GitHub Actions es el
motor típico.
"""),
"nube": ("la nube / cloud", """
**La nube** son computadoras de otro que rentas por hora: AWS, Azure,
GCP te prestan máquinas, redes y servicios administrados. Pagas por no
comprar hardware — y por no administrarlo tú.
"""),
"region": ("región / zona de disponibilidad", """
Una **región** es una ubicación geográfica del proveedor (`us-east-1`,
`brazil-south`): elige la cercana a tus usuarios. Dentro, las
**zonas de disponibilidad** son datacenters separados — tu app sobrevive
que se caiga uno.
"""),
"iaas-paas-saas": ("IaaS / PaaS / SaaS", """
**IaaS**: rentas la máquina, administras todo lo de adentro.
**PaaS**: rentas la plataforma, solo traes tu código. **SaaS**: usas el
software hecho (Gmail, RDS administrado). Menos control, menos trabajo.
"""),
"serverless": ("serverless / función", """
**Serverless** = no piensas en servidores: subes una *función* y el
proveedor la ejecuta por evento, escalando de 0 a 1000 sola. Pagas por
ejecución. Lambda (AWS), Cloud Functions (GCP), Azure Functions.
"""),
"cold-start": ("cold start", """
El **cold start** es el precio de serverless: si nadie llamó a tu
función hace rato, el proveedor la "despierta" — eso tarda 100ms–2s
extra. Funciones calientes responden al instante.
"""),
"vm": ("máquina virtual (VM)", """
Una **VM** es una computadora simulada completa sobre hardware real:
su propio SO, su kernel, su disco. Más pesada que un contenedor (que
comparte kernel) pero el aislamiento es total.
"""),
"on-premise": ("on-premise / datacenter", """
**On-premise** = servidores propios en tu edificio o un datacenter
rentado: tú compras, enchufas, enfrías y reemplazas. Lo contrario de
cloud — más control físico, mucha más operación.
"""),
"kubernetes": ("Kubernetes (k8s)", """
**Kubernetes** es el orquestador de contenedores: le dices "quiero 3
réplicas de esta imagen" y él las distribuye, reinicia las que mueren
y las expone. Poderoso y complejo — se usa cuando las máquinas ya son
manada.
"""),
"load-balancer": ("load balancer", """
Un **load balancer** reparte el tráfico entre tus réplicas: request
entra → lo manda a la instancia menos ocupada. Además detecta cuál
está caída (health checks) y deja de enviarle.
"""),
"vpc": ("VPC / red privada", """
Una **VPC** (Virtual Private Cloud) es tu red privada dentro de la
nube: la BD vive en la subred privada que internet no ve; solo el load
balancer tiene cara pública. Es el muro interior.
"""),
"firewall": ("firewall / security group", """
Un **firewall** (security group en AWS) es la lista de puertos que
aceptan tráfico: "443 abierto a todos, 5432 solo desde la app". Cada
puerto abierto es una puerta a vigilar — abre lo mínimo.
"""),
"ssh": ("SSH", """
**SSH** es el túnel cifrado para entrar a un servidor remoto y usar su
terminal: `ssh usuario@servidor`. Es como control remoto por texto —
con llaves, no contraseñas (la llave es la identidad).
"""),
"bucket": ("bucket / object storage", """
Un **bucket** (S3, Azure Blob, GCS) es almacenamiento de archivos como
servicio: subes un PDF/imagen, te devuelve una URL. No es un disco —
no lo montas, lo consultas por HTTP. Barato, infinito, durable.
"""),
"websocket": ("WebSocket", """
**WebSocket** es una conexión que queda *viva*: en vez de preguntar-
responder-cerrar como HTTP, ambos pueden hablar cuando quieran. Es
como el servidor puede *empujar* — por eso sirve para chat y
colaboración en vivo.
"""),
"webhook": ("webhook", """
Un **webhook** es una llamada HTTP invertida: en vez de tú preguntarle
a Stripe "¿llegó el pago?", Stripe te llama a tu endpoint cuando pasa.
Se verifica la firma (es público) y se responde 200 rápido.
"""),
"job": ("background job / cola", """
Un **job** es trabajo que se hace sin que el usuario espere: mandar el
email, generar el PDF. Va a una **cola** y un *worker* lo procesa en
segundo plano — la respuesta HTTP sale inmediata.
"""),
"retry": ("retry / backoff", """
Un **retry** es reintentar lo que falló — las redes fallan, es normal.
**Backoff** = esperar más cada vez (1s, 2s, 4s…): evita martillar a un
servicio que ya está sufriendo.
"""),
"timeout": ("timeout", """
Un **timeout** es la fecha límite de una espera: "si la BD no responde
en 5s, falla". Sin timeout, un servicio caído convierte tu espera en
infinita — tu app muere de pie esperando.
"""),
"idempotencia": ("idempotencia", """
**Idempotencia** = repetir la operación da el mismo resultado que una
vez. `POST /pay` con `Idempotency-Key: abc` ejecutado dos veces cobra
una. Vital porque clientes y webhooks *siempre* reintentan.
"""),
"mock": ("mock / stub", """
Un **mock** es un doble de pruebas: finge ser el servicio externo
(Stripe, SMTP) para que el test no cobre ni mande emails. Se mockea en
la *frontera* (tu adaptador), nunca la BD — fingir la BD es mentir el
test.
"""),
"tdd": ("TDD", """
**TDD** (Test-Driven Development) = escribir el test *antes* del código:
primero defines qué debe pasar (rojo), luego lo haces pasar (verde),
luego limpias. El test es la especificación que corre.
"""),
"cobertura": ("cobertura (coverage)", """
La **cobertura** es el % de tu código que los tests ejecutan. Útil como
detector de "esto nadie lo prueba"; inútil como meta — 90% cubierto no
significa que los tests afirmen algo correcto.
"""),
"rollback": ("rollback", """
Un **rollback** es volver atrás: la migración se revierte, el deploy
regresa a la versión anterior. Todo cambio serio tiene plan de rollback
*antes* de ejecutarse — si no, el plan es rezar.
"""),
"healthcheck": ("health check", """
Un **health check** es el endpoint `/health` donde la app dice "estoy
viva". El orquestador/load balancer lo consulta cada pocos segundos:
si falla, reinicia la instancia o deja de mandarle tráfico.
"""),
"observabilidad": ("observabilidad", """
**Observabilidad** = poder responder "¿qué está pasando adentro?" sin
reproducirlo: logs (qué pasó), métricas (cuánto), trazas (por dónde
viajó el request). Son las tres patas.
"""),
"metricas": ("métricas", """
Las **métricas** son números que la app reporta: requests/segundo,
latencia p95, errores. A diferencia del log (un evento), la métrica
es la tendencia — la alarma suena cuando el número se sale de rango.
"""),
"tracing": ("trazas (tracing)", """
Una **traza** sigue un request a través de todo el sistema: entró por
el gateway → llamó auth → consultó la BD → tardó 340ms en la query.
Cuando algo anda lento, la traza dice exactamente dónde.
"""),
"percentil": ("p95 / p99", """
**p95** = el request en el percentil 95: el 95% de los requests fueron
más rápidos que él. Importa más que el promedio — el promedio esconde
que el 1% de tus usuarios espera 10 segundos.
"""),
"postmortem": ("postmortem", """
Un **postmortem** es la autopsia escrita de un incidente: qué pasó,
por qué (la causa raíz, no "alguien tocó mal"), y qué cambia para que
no vuelva. Sin culpar — el sistema permitió el error.
"""),
"yaml": ("YAML", """
**YAML** es el formato de configuración de la industria: texto con
indentación para jerarquía. Compose, GitHub Actions y Kubernetes lo
usan. Regla de oro: la indentación *es* la estructura — un espacio mal
puesto rompe todo.
"""),
"blue-green": ("blue-green / rolling / canary", """
Estrategias de deploy sin downtime: **blue-green** = levantas la versión
nueva completa y cambias el tráfico de golpe; **rolling** = reemplazas
réplicas de a una; **canary** = el 5% de usuarios prueba primero.
"""),
"replica": ("réplica / failover", """
Una **réplica** es una copia de la BD que sigue a la principal en
tiempo real. Si la principal muere, el *failover* promueve la réplica —
el servicio parpadea en vez de caer.
"""),
"backup": ("backup / respaldo", """
Un **backup** es una copia de los datos en otro lugar, hecha seguido y
*probada* (un backup que nunca se restauró no es backup, es esperanza).
Regla 3-2-1: 3 copias, 2 medios, 1 fuera del sitio.
"""),
"terraform": ("Terraform / IaC", """
**Terraform** describe la infraestructura como código: "quiero una VPC,
2 VMs y una BD" en archivos versionables. *Infraestructura como código*
= la infra se revisa en PR y se recrea igual cada vez.
"""),
"monolito": ("monolito", """
Un **monolito** es una app donde todo corre en un solo proceso: rutas,
lógica, BD access. No es insulto — es el default correcto mientras el
equipo sea chico. Se puede modular por dentro sin dividir el deploy.
"""),
"microservicio": ("microservicios", """
**Microservicios** = dividir la app en servicios independientes que se
comunican por red. Ganas despliegue separado; pagas con distribución
(transacciones entre servicios, latencia, observabilidad). Equipo de 5
no necesita esto.
"""),
"escalado": ("escalado horizontal / vertical", """
**Vertical**: máquina más gorda (más CPU/RAM) — fácil, tiene techo.
**Horizontal**: más máquinas — el camino de internet, pero requiere que
la app no guarde estado local (por eso todo va a BD/Redis).
"""),
"latencia": ("latencia / throughput", """
**Latencia** = cuánto tarda UNA operación (ms). **Throughput** =
cuántas haces por segundo. Se pelean: bajar latencia no siempre sube
throughput. La latencia la siente el usuario; el throughput lo paga tu
factura.
"""),
"estado": ("estado (state)", """
El **estado** es todo lo que el programa recuerda: las variables, la
sesión, lo que muestra la UI. *Stateless* (sin estado) = el servidor no
recuerda nada entre requests — cada request trae todo lo necesario.
"""),
"evento": ("evento", """
Un **evento** es "algo que pasó" convertido en dato: el click del
usuario, el `payment.succeeded` del webhook, el mensaje del socket.
La programación moderna es reaccionar a eventos más que seguir un guion.
"""),
"recurso": ("recurso (REST)", """
Un **recurso** es la "cosa" que tu API maneja: `tasks`, `users`,
`projects`. Las URLs los nombran (`/tasks/5`), los verbos actúan sobre
ellos. Diseñar REST = nombrar bien tus recursos.
"""),
"dom": ("DOM", """
El **DOM** es la página como árbol de objetos vivos: HTML es el papel,
el DOM es lo que JavaScript puede tocar. `element.textContent = "hola"`
cambia el DOM y el navegador repinta — el HTML original no se entera.
"""),
"dev-server": ("dev server / hot reload", """
El **dev server** (Vite, `npm run dev`) sirve tu app mientras
desarrollas y recarga el navegador al guardar — *hot reload*. No es el
servidor de producción: es la mesa de trabajo.
"""),
"transpilador": ("transpilador", """
Un **transpilador** traduce entre lenguajes de mismo nivel: TypeScript
→ JavaScript, JSX → JS. El navegador solo entiende JS estándar; el
transpilador convierte tu código cómodo en código que corre.
"""),
"semver": ("versionado semántico (semver)", """
**Semver** = `MAJOR.MINOR.PATCH` (`2.4.1`): major rompe, minor agrega
compatible, patch arregla. Por eso `^2.4.1` en package.json = "dame
compatible, no me rompas".
"""),
"gzip": ("gzip / compresión", """
**gzip** comprime las respuestas antes de viajar: el JSON de 500KB
cruza como 50KB. El navegador descomprime transparente — gratis de
activar en el proxy, obligatorio en texto.
"""),
"deadlock": ("deadlock", """
Un **deadlock** es el abrazo mortal: la tx A tiene el lock de la fila 1
y pide la 2; la tx B tiene la 2 y pide la 1. Nadie avanza. La BD mata a
una — por eso los locks se toman siempre en el mismo orden.
"""),
"pub-sub": ("pub/sub", """
**Pub/sub** = publicar-suscribir: quien emite un mensaje no sabe quién
lo lee; los suscriptores reciben lo que les interesa. Redis pub/sub
conecta instancias de tu app (para broadcast de WebSockets entre
réplicas, por ejemplo).
"""),
"crdt": ("CRDT", """
Un **CRDT** es una estructura de datos que se fusiona sola: dos personas
editan sin coordinarse y al converger ambos ven lo mismo. Así Figma y
Google Docs fusionan sin lock — poderoso y bastante complejo.
"""),
"cascade": ("ON DELETE CASCADE", """
**CASCADE** = borrar en cadena: al borrar el proyecto se borran sus
tareas automáticamente. Conveniente y peligroso — un borrado en la
tabla equivocada se lleva medio mundo. RESTRICT es más seguro.
"""),
# --- Basic programming terms (reader starts from zero) ---
"variable": ("variable", """
Una **variable** es una caja con nombre donde guardas un valor:
`let total = 42` guarda el 42 bajo el nombre `total`. Puedes leerla y
cambiarla después (`total = 50`). `const` = caja que no se puede
reemplazar.
"""),
"funcion": ("función", """
Una **función** es una receta reutilizable: recibe ingredientes
(parámetros), hace pasos y devuelve un plato (`return`). La escribes
una vez y la llamas mil veces: `add(2, 3)` → `5`.
"""),
"parametro": ("parámetro / argumento", """
El **parámetro** es el hueco declarado en la función (`def f(x)` — `x`
es parámetro); el **argumento** es el valor concreto que le pasas
(`f(42)` — `42` es argumento). Mismo dato, dos momentos: declaración
vs uso.
"""),
"array": ("array / lista / slice", """
Un **array** es una colección ordenada de elementos accedidos por
posición: `["a","b","c"][0]` es `"a"` (se cuenta desde 0). Python las
llama *listas*, Go *slices* — misma idea, distinto acento.
"""),
"objeto": ("objeto / dict / struct", """
Un **objeto** es una colección de datos con nombre: `{name: "Ana",
age: 30}` — cada dato es una *propiedad* (clave → valor). Python los
llama `dict`, Go los arma con `struct`, TS con objetos/`interface`.
"""),
"bucle": ("bucle (loop)", """
Un **bucle** repite una acción por cada elemento o hasta cumplir una
condición: `for task in tasks` hace algo con cada tarea. `map` y
`filter` son bucles disfrazados de funciones — transforman/filtran
colecciones sin `for` explícito.
"""),
"condicional": ("condicional (if/else)", """
Un **condicional** es la bifurcación del código: `if condición` hace
una cosa, `else` hace otra. Es donde el programa "decide" — la lógica
de negocio vive casi toda en condicionales.
"""),
"clase": ("clase / struct", """
Una **clase** es el molde de un objeto: define qué datos y qué métodos
tiene. `class Task` es el molde; `new Task()` es una instancia concreta.
Go no tiene clases — usa `struct` + métodos sueltos.
"""),
"string": ("string", """
Un **string** es texto entre comillas: `"hola"`. El nombre viene de
"cadena de caracteres" — una secuencia de letras. Todo lo que llega de
un formulario o una URL llega como string, aunque parezca número.
"""),
"booleano": ("booleano", """
Un **booleano** es un valor de dos estados: `true` o `false`. Es el
resultado de toda comparación (`age > 18`) y lo que los `if` evalúan.
Nombrado por George Boole, el matemático de la lógica.
"""),
"null": ("null / None / nil", """
**null** (TS), `None` (Py), `nil` (Go) = "aquí no hay valor". Es la
respuesta a "¿qué devuelvo cuando no hay nada?" — y la fuente del bug
más famoso de la historia (su inventor lo llamó "el error del billón
de dólares"). Por eso el código revisa `if x is not None`.
"""),
"return": ("return", """
**return** hace dos cosas a la vez: devuelve el resultado Y termina la
función — lo que esté debajo nunca corre. `return task` = "aquí está el
plato, salgo de la cocina".
"""),
"asincrono": ("asíncrono", """
**Asíncrono** = empezar algo sin esperar sentado a que termine: pides
la pizza (async) y sigues trabajando; cuando llega, te avisan. Lo
opuesto a síncrono (esperar parado). Vital cuando la espera es larga:
red, disco, bases de datos.
"""),
"callback": ("callback", """
Un **callback** es una función que entregas para que otra la llame
después: `button.onClick(mostrarAlerta)` = "cuando haya click, llama
a esto". Es el patrón base de los eventos; async/await es su forma
moderna más legible.
"""),
"goroutine": ("goroutine", """
Una **goroutine** es el hilo ultraligero de Go: `go f()` lanza una
función en paralelo gastando casi nada — se pueden tener millones. Es
la superpotencia de Go: concurrencia como palabra del lenguaje.
"""),
"metodo": ("método", """
Un **método** es una función que vive dentro de un objeto/clase:
`task.save()` — `save` es un método de `task`. La diferencia con una
función suelta: el método conoce al objeto que lo contiene (`this`/
`self`).
"""),
"diccionario": ("diccionario / map", """
Un **diccionario** (`dict` en Python, `map` en Go, objeto en JS) guarda
parejas clave→valor: `{"ana": 30}`. Es la estructura que más aparece
en JSON — un objeto JS *es* un diccionario.
"""),
"tupla": ("tupla", """
Una **tupla** es una colección ordenada que no se puede cambiar:
`(200, "OK")` — el número de elementos y su orden son fijos. Go devuelve
`(valor, error)` en todo lado; es una tupla de facto.
"""),
"compilado": ("lenguaje compilado vs interpretado", """
**Compilado** (Go): el código se traduce a binario una vez y ese binario
corre solo — rápido, deploy simple. **Interpretado** (Python, JS): un
runtime lee el código en cada ejecución — flexible, pero necesita el
runtime instalado.
"""),
}

os.makedirs(OUT, exist_ok=True)
for slug, (term, body) in EXPLAIN.items():
    body = textwrap.dedent(body).strip()
    content = (
        f'::: {{.callout-tip collapse="true" title="Explicación de: {term}"}}\n'
        f"{body}\n"
        f":::\n"
    )
    with open(os.path.join(OUT, f"{slug}.md"), "w", encoding="utf-8") as f:
        f.write(content)
print(f"{len(EXPLAIN)} explanation files written to {OUT}/")
