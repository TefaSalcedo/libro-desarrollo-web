# Inserts "EXTRA" external-roadmap callouts into the right chapters.
# Each block is a collapsible callout with the blue EXTRA tag badge.
import io

BLOCKS = {
"capitulos/cap-02.qmd": """::: {.callout-note collapse="true" title="EXTRA · El panorama de lenguajes backend"}

<span class="tag tag-extra">EXTRA</span> Curado de roadmaps externos
(roadmap.sh, guías de bootcamp): los lenguajes que verás en el mercado,
con su reputación honesta —

- **Go** — moderno y simple; rendimiento general excelente
- **Python** — elegante, ideal para apps backend sencillas
- **JavaScript / Node.js** — serial para aplicaciones web; desarrolladores de sobra
- **Java** — código más complejo, pero increíblemente rápido
- **C#** — excelente si trabajas en el ecosistema Microsoft
- **Ruby** — bueno si quieres Rails y te gusta ese estilo
- **PHP** — excelente para sitios web simples; menos para APIs

El libro elige TypeScript + Python + Go porque entre los tres cubren
casi todos los modelos (event loop, async/GIL, goroutines). No hay
elección "correcta" — hay el que tu equipo y tu mercado local usan.
*→ cap-40 compara a fondo.*
:::""",
"capitulos/cap-03.qmd": """::: {.callout-note collapse="true" title="EXTRA · Frameworks que te encontrarás fuera"}

<span class="tag tag-extra">EXTRA</span> El libro usa Express, FastAPI y
Go estándar, pero el ecosistema real es más amplio. Roadmaps externos
recomiendan conocer —

- **Ruby on Rails** — "convención sobre configuración", testing
  integrado, localización; open source escrito en Ruby
- **Django** (Python) — "baterías incluidas": auth, admin, ORM; hoy
  también async
- **Flask** (Python) — microframework minimalista, servidor de
  desarrollo integrado, rápido para prototipar
- **Express** (Node) — ligero y adaptable; depuración y desarrollo de
  servidores rápidos

Mismo patrón en todos: rutas → handlers → middleware. Si entiendes el
de este libro, lees cualquiera de estos en una tarde.
:::""",
"capitulos/cap-07.qmd": """::: {.callout-note collapse="true" title="EXTRA · Patrones arquitectónicos del roadmap"}

<span class="tag tag-extra">EXTRA</span> Las taxonomías de arquitectura
que listan los roadmaps backend —

- **Monolítico** — todo en un proceso; el default correcto al empezar
- **Microservicios** — procesos separados por dominio; paga cuando el
  equipo ya no cabe en un monolito
- **Serverless** — funciones por evento, sin servidor visible
- **Escalado vertical** (máquina más grande) vs **horizontal** (más
  máquinas — exige app sin estado local)
- **Balanceadores de carga** — reparten el tráfico entre réplicas

Todos aparecen como capítulos o decisiones en este libro; la lista sirve
de mapa de vocabulario para reconocerlos en una entrevista. *→ cap-30..35,
nu-05, Ap. K.*
:::""",
"capitulos/cap-08.qmd": """::: {.callout-note collapse="true" title="EXTRA · El paisaje completo de bases de datos"}

<span class="tag tag-extra">EXTRA</span> Lo que los roadmaps listan como
bases que debes reconocer —

**Relacionales:** MySQL (la más popular históricamente), PostgreSQL,
MariaDB, MS SQL Server, Oracle.

**NoSQL:** MongoDB, CouchDB, DynamoDB (RethinkDB quedó en el camino).
Muchas startups optan por NoSQL — pero la decisión es por *forma del
dato*, no por moda (ver la sección anterior de este capítulo).

El libro elige PostgreSQL: relacional completo, JSONB cuando el dato
varía, y el mismo motor en local y producción.
:::""",
"capitulos/cap-12.qmd": """::: {.callout-note collapse="true" title="EXTRA · Las estructuras de datos detrás de tu BD"}

<span class="tag tag-extra">EXTRA</span> Los roadmaps piden "estructuras
de datos y algoritmos" — aquí está por qué les importa a un backend,
conectado con lo que acabas de ver:

- **Tabla hash** → así funciona un índice `HASH`
- **Árbol de búsqueda (BST)** → el B-tree de los índices normales es su
  primo balanceado; por eso la búsqueda es O(log n)
- **Búsqueda binaria** → la misma idea: descartar la mitad en cada paso
- **Arreglos / listas enlazadas / pilas / colas / grafos** → el lenguaje
  de la entrevista; las colas son literalmente los jobs del cap-21
- **Recursión y ordenamientos** (burbuja, selección, inserción) →
  ejercicio clásico; en la vida real ordena la BD con `ORDER BY` + índice

No necesitas implementar un árbol rojo-negro; necesitas *reconocer* qué
estructura usa cada herramienta — eso es lo que hace predecible el
rendimiento.
:::""",
"capitulos/cap-14.qmd": """::: {.callout-note collapse="true" title="EXTRA · El mapa de hashing y seguridad web"}

<span class="tag tag-extra">EXTRA</span> Los roadmaps piden "entender la
seguridad web" — el mapa completo, ubicado:

- **MD5** — roto; nunca para contraseñas (solo checksums)
- **Familia SHA** — integridad y firmas; demasiado rápida para passwords
- **scrypt** — alternativa seria a bcrypt, también lenta a propósito
- **bcrypt** — la de este capítulo: lenta + salt incorporado
- **HTTPS / SSL / TLS** — el canal cifrado (cap-33 lo sirve)
- **CORS** — política de orígenes del navegador (cap-18)

Regla que no caduca: contraseñas → bcrypt/scrypt/argon2; integridad →
SHA/HMAC; MD5 → solo para verificar que un archivo no se corrompió.
:::""",
"capitulos/cap-27.qmd": """::: {.callout-note collapse="true" title="EXTRA · Los tres niveles que nombran los roadmaps"}

<span class="tag tag-extra">EXTRA</span> Cuando un roadmap o una
entrevista dice "tipos de pruebas", se refiere a —

- **Pruebas unitarias** — una función aislada, sin BD ni red (cap-27)
- **Pruebas de integración** — la API contra la BD real (cap-28)
- **Pruebas funcionales / e2e** — el sistema completo como un usuario
  (cap-27, la punta cara de la pirámide)

La pirámide del libro ordena exactamente esto: muchas unitarias, las
suficientes de integración, pocas funcionales.
:::""",
"capitulos/cap-30.qmd": """::: {.callout-note collapse="true" title="EXTRA · Containerización / virtualización"}

<span class="tag tag-extra">EXTRA</span> El roadmap externo lista —
**Docker** (el estándar de contenedores, este capítulo), **Kubernetes**
(orquestador de manadas de contenedores — nu-05 lo ubica), **rkt**
(histórico, ya descontinuado — buen recordatorio de que las listas
envejecen y los conceptos quedan).
:::""",
"capitulos/cap-33.qmd": """::: {.callout-note collapse="true" title="EXTRA · Servidores web del mundo real"}

<span class="tag tag-extra">EXTRA</span> Los roadmaps piden conocer
servidores web — el trio real:

- **Nginx** — el reverse proxy estándar: sirve estáticos rapidísimo y
  reparte a tu app
- **Apache** — el veterano; `.htaccess` y hosting clásico
- **Reverse proxy** — el *rol*, no un producto: terminar TLS, servir
  estáticos, balancear; Nginx/Caddy/Traefik lo juegan

Tu app (Node/Python/Go) nunca mira internet directamente — el proxy es
su fachada.
:::""",
"capitulos/cap-terminal.qmd": """::: {.callout-note collapse="true" title="EXTRA · Control de versiones y dónde viven los repos"}

<span class="tag tag-extra">EXTRA</span> Los roadmaps piden dos cosas:
*comandos básicos de Git* (clone, add, commit, push, pull, branch,
merge) y *servicios de alojamiento de repositorios*:

- **GitHub** — la comunidad más grande; donde vive el open source y tu
  portafolio
- **GitLab** — ciclo completo en una plataforma (repos + CI/CD + issues)
- **Bitbucket** — el clásico del ecosistema Atlassian
- **AWS CodeCommit** — repos Git privados administrados por Amazon

El cometario que vale: tu perfil de GitHub *es* tu portafolio — los
equipos que contratan lo miran antes que el CV.
:::""",
"capitulos/nu-01.qmd": """::: {.callout-note collapse="true" title="EXTRA · Fundamentos de internet (el checklist del roadmap)"}

<span class="tag tag-extra">EXTRA</span> Antes de servidores, los
roadmaps piden entender internet misma — cada ítem mapea a un capítulo:

- ¿Cómo funciona internet? — paquetes que viajan entre IPs
- ¿Qué es HTTP y HTTPS? — *cap-01, cap-33*
- ¿Qué es una dirección IP? — *este capítulo*
- ¿Qué es un nombre de dominio? ¿DNS? — *cap-33, nu-04*
- ¿Qué es hosting? — *nu-02*
- ¿Qué es SMTP? — el protocolo de correo; por eso mandar email es un job
  externo (*cap-21*)
:::""",
"capitulos/nu-04.qmd": """::: {.callout-note collapse="true" title="EXTRA · Las tres capas de caché del roadmap"}

<span class="tag tag-extra">EXTRA</span> Cuando un roadmap dice
"aprende caching", son tres capas distintas —

- **CDN** — la copia en el borde, cerca del usuario (*este capítulo*)
- **Caché del lado del servidor** — Redis o Memcached: resultados de
  queries caras, sesiones, rate limits
- **Caché del lado del cliente** — el navegador guarda estáticos con
  headers de expiración

El libro lo deja como decisión (Ap. K #14): el caché se agrega cuando un
problema *medido* lo pide — antes es complejidad sin beneficio.
:::""",
"capitulos/ap-j.qmd": """::: {.callout-note collapse="true" title="EXTRA · Lo que los roadmaps dicen sobre carrera"}

<span class="tag tag-extra">EXTRA</span> Más allá del código, las guías
externas coinciden en lo no-técnico —

- **Resolver problemas y comunicación**: el trabajo no termina en código
  correcto; hay que explicar soluciones al equipo y a otros departamentos
- **Portafolio**: perfil de GitHub activo + proyectos de código abierto
- **Networking**: LinkedIn, meetups, conferencias — "la conexión correcta
  puede ser la diferencia entre quedarte y conseguir el trabajo soñado"
- **Voluntariado/open source**: experiencia real visible para
  empleadores mientras no tienes empleo
- **Recursos de aprendizaje**: freeCodeCamp (introducción gratuita), Khan
  Academy (fundamentos), MDN Web Docs (tutoriales por nivel), libros como
  *JavaScript Professional* (Zakas) y cursos prácticos de Node.js
  (Andrew Mead)

El hilo que los une: *aprendizaje basado en proyectos* — construir cosas
reales retiene más que la teoría sola. Es literalmente el diseño de este
libro.
:::""",
}

import re

anchors = ['## Ejercicio', '## Mini reto', '## Lo que deberías saber hacer ahora']

for path, block in BLOCKS.items():
    txt = open(path, encoding='utf-8').read()
    if 'tag-extra' in txt:
        continue  # idempotent
    pos = -1
    for a in anchors:
        i = txt.find(a)
        if i != -1:
            pos = i
            break
    if pos == -1:
        txt += '\n\n' + block + '\n'
    else:
        txt = txt[:pos].rstrip('\n') + '\n\n' + block + '\n\n' + txt[pos:]
    open(path, 'w', encoding='utf-8').write(txt)
    print('EXTRA ->', path)

print('done')
