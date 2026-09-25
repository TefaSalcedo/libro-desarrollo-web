# Inserts {{< include _explicaciones/SLUG.md >}} into each chapter at the
# first safe paragraph where the term appears. Fallback: grouped block
# before the final checklist section.
import json, re, glob, os

# Same patterns used for scanning (term -> regex)
TERMS = {
 'runtime': r'\bruntime\b|tiempo de ejecución',
 'entorno': r'\bentornos?\b',
 'dom': r'\bDOM\b',
 'framework': r'\bframeworks?\b',
 'dependencia': r'\bdependencias?\b',
 'build': r'\bbuild\b',
 'dev-server': r'\bdev server\b|servidor de desarrollo',
 'compilador': r'\bcompil\w+\b',
 'terminal': r'\bterminal\b|\bconsola\b',
 'cli': r'\bCLI\b|línea de comandos',
 'path': r'\bPATH\b',
 'git': r'\bGit\b',
 'commit': r'\bcommits?\b',
 'repositorio': r'\brepositorios?\b|\brepo\b',
 'puerto': r'\bpuertos?\b|:3000|:5432|:8080',
 'localhost': r'\blocalhost\b|127\.0\.0\.1',
 'proceso': r'\bprocesos?\b',
 'memoria': r'\bmemoria\b|\bRAM\b',
 'cpu': r'\bCPU\b|\bnúcleos?\b|cores?\b',
 'base-de-datos': r'\bbases? de datos\b|\bBD\b',
 'query': r'\bquer\w+\b|\bconsultas?\b',
 'esquema': r'\besquemas?\b|\bschema\b',
 'indice': r'\bíndices?\b|\bIndex Scan\b|\bSeq Scan\b',
 'migracion': r'\bmigraci\w+\b',
 'transaccion': r'\btransacci\w+\b|\btx\b|\bACID\b',
 'pool': r'\bpools?\b',
 'orm': r'\bORM\b',
 'join': r'\bJOINs?\b',
 'foreign-key': r'\bforeign keys?\b|clave foránea|\bFK\b',
 'autenticacion': r'\bautenticaci\w+\b|\bauth\b|\blogin\b',
 'autorizacion': r'\bautorizaci\w+\b|\bpermisos?\b',
 'sesion': r'\bsesiones?\b|\bsession\b',
 'cookie': r'\bcookies?\b',
 'token': r'\btokens?\b',
 'jwt': r'\bJWT\b',
 'hash': r'\bhash\w*\b|\bbcrypt\b',
 'cifrado': r'\bcifrad\w+\b|encript\w+',
 'firma': r'\bfirmas?\b|\bHMAC\b',
 'middleware': r'\bmiddlewares?\b',
 'log': r'\blogs?\b|\blogging\b|\blogger\b',
 'variable-de-entorno': r'\bvariables? de entorno\b|env vars|\b\.env\b|env\.',
 'secreto': r'\bsecretos?\b|\bsecret\b',
 'deploy': r'\bdeploy\w*\b|desplieg\w+',
 'servidor': r'\bservidores?\b|\bserver\b',
 'dns': r'\bDNS\b',
 'dominio': r'\bdominios?\b',
 'ip': r'\bIP\b|dirección IP',
 'tls': r'\bHTTPS\b|\bTLS\b|\bSSL\b|certificado',
 'proxy': r'\bproxy\b',
 'cdn': r'\bCDN\b',
 'cache': r'\bcach\w+\b|\bRedis\b',
 'docker': r'\bDocker\b',
 'contenedor': r'\bcontenedores?\b|\bcontainer\b',
 'imagen': r'\bimagen\w*\b',
 'volumen': r'\bvolúmenes?\b|\bvolumes?\b',
 'compose': r'\bcompose\b|docker compose',
 'registry': r'\bregistro\b|\bregistry\b|Docker Hub|\bECR\b',
 'cicd': r'\bCI/CD\b|\bpipeline\b|GitHub Actions',
 'nube': r'\bnube\b|\bcloud\b|\bAWS\b|\bAzure\b|\bGCP\b',
 'region': r'\bregiones?\b|\bregion\b|\bAZ\b',
 'iaas-paas-saas': r'\bIaaS\b|\bPaaS\b|\bSaaS\b',
 'serverless': r'\bserverless\b|\bLambda\b|\bFaaS\b',
 'cold-start': r'\bcold.?start\b|arranque en fr\w+',
 'websocket': r'\bWebSockets?\b',
 'webhook': r'\bwebhooks?\b',
 'job': r'\bjobs?\b|\bcolas?\b|\bworkers?\b|background',
 'concurrencia': r'\bconcurrenci\w+\b|concurrente|paralel\w+',
 'asincrono': r'\bas[íi]ncron\w+\b|async/await|\bPromise\b|\bawait\b',
 'hilo': r'\bhilos?\b|\bthreads?\b|goroutines?\b',
 'latencia': r'\blatencia\b|throughput',
 'escalado': r'\bescal\w+\b|horizontal|vertical',
 'staging': r'\bstaging\b',
 'produccion': r'\bproducci\w+\b|\bprod\b',
 'n-mas-1': r'\bN\+1\b',
 'paginacion': r'\bpaginaci\w+\b|\bLIMIT\b|\boffset\b|\bcursor\b',
 'monolito': r'\bmonolitos?\b',
 'microservicio': r'\bmicroservicios?\b',
 'idempotencia': r'\bidempoten\w+\b',
 'retry': r'\bretry\b|reintentos?\b|\bbackoff\b',
 'timeout': r'\btimeouts?\b',
 'mock': r'\bmocks?\b|\bstubs?\b',
 'tdd': r'\bTDD\b|test.driven',
 'cobertura': r'\bcobertura\b|coverage',
 'rollback': r'\brollbacks?\b',
 'healthcheck': r'\bhealth.?check\w*\b|/health\b',
 'crud': r'\bCRUD\b',
 'openapi': r'\bOpenAPI\b',
 'adr': r'\bADRs?\b',
 'regex': r'\bregex\b|expresi\w+ regular',
 'ssh': r'\bSSH\b',
 'firewall': r'\bfirewalls?\b|\bufw\b|security group',
 'load-balancer': r'\bload.?balanc\w+\b|balanceador',
 'vpc': r'\bVPC\b|red privada|subred',
 'bucket': r'\bbuckets?\b|object storage|\bS3\b|Blob Storage',
 'secret-manager': r'\bsecret managers?\b|Secrets Manager|Key Vault',
 'rate-limit': r'\brate.?limit\w*\b|\b429\b',
 'cors': r'\bCORS\b',
 'xss': r'\bXSS\b|\bCSRF\b|cross.site',
 'roles': r'\broles?\b|\bRBAC\b|\badmin\b|\bviewer\b|\beditor\b',
 'lock': r'\bbloqueos?\b|\block\b|FOR UPDATE',
 'snapshot': r'\bsnapshots?\b',
 'diff': r'\bdiffs?\b',
 'recurso': r'\brecursos?\b|resource',
 'estado': r'\bestados?\b|\bstate\b',
 'evento': r'\beventos?\b|\bevent\b',
 'transpilador': r'\btranspil\w+\b',
 'semver': r'\bsemver\b|versionado semántico',
 'on-premise': r'\bon.?premise\b|datacenter|centro de datos',
 'vm': r'\bVMs?\b|máquina virtual|virtualizaci\w+',
 'kubernetes': r'\bKubernetes\b|\bk8s\b|orquestador',
 'pub-sub': r'\bpub/sub\b',
 'crdt': r'\bCRDTs?\b',
 'deadlock': r'\bdeadlocks?\b',
 'constraint': r'\bconstraints?\b|restricci\w+',
 'gzip': r'\bgzip\b|compresi\w+',
 'owasp': r'\bOWASP\b',
 'inyeccion-sql': r'\binyecci\w+ SQL\b|SQL injection|parametrizad\w+',
 'replica': r'\bréplicas?\b|failover',
 'backup': r'\bbackups?\b|respaldo',
 'terraform': r'\bTerraform\b|\bIaC\b|infraestructura como c\w+',
 'yaml': r'\bYAML\b|\.ya?ml\b',
 'multi-stage': r'\bmulti.?stage\b',
 'blue-green': r'\bblue.?green\b|canary|rolling',
 'observabilidad': r'\bobservabil\w+\b',
 'metricas': r'\bmétricas?\b|\bmetrics\b|\bprometheus\b',
 'tracing': r'\btrazas?\b|\btracing\b|\bspan\b',
 'percentil': r'\bp95\b|\bp99\b|percentil',
 'postmortem': r'\bpostmortem\b',
 'code-review': r'\bcode review\b|revisión de código',
 'pull-request': r'\bpull requests?\b|\bPRs?\b|\bmerge\b|rebase|squash',
 'callback': r'\bcallbacks?\b',
 'modulo': r'\bmódulos?\b|\bimport\b|\brequire\b',
 'serializar': r'\bserializ\w+\b|stringify|\bparse\b',
 'stdout': r'\bstdout\b|\bstdin\b|\bstderr\b',
 'goroutine': r'\bgoroutines?\b',
 'gil': r'\bGIL\b',
 'event-loop': r'\bevent loop\b',
 'api': r'\bAPIs?\b',
 'endpoint': r'\bendpoints?\b',
 'json': r'\bJSON\b|\bJSONB\b',
 'request': r'\brequests?\b|peticiones?\b',
 'async-await': r'\basync\b|\bawait\b|\bPromise\b',
 'array': r'\barrays?\b|\blistas?\b|\bslices?\b',
 'objeto': r'\bobjetos?\b|\bobject\b|\bstruct\b|\binterface\b',
 'tipado': r'\btipos?\b|\btype\b|\bint\b|\bstring\b|\bboolean\b',
 'funcion': r'\bfunciones?\b|\bfunction\b|\bdef\b|\bfunc\b',
 'variable': r'\bvariables?\b|\blet\b|\bconst\b|\bvar\b',
 'bucle': r'\bbucles?\b|\bloop\b|\bfor\b|\bwhile\b|\bmap\b|\bfilter\b',
 'paquete': r'\bpaquetes?\b|\bpackage\b|\bnpm\b|\bpip\b|\bgo mod\b',
 'cliente': r'\bclientes?\b|\bclient\b',
 'cascade': r'\bCASCADE\b',
 'sesion': r'\bsesiones?\b|\bsession\b',
}

# Priority order: foundational first (insertion cap picks these first)
PRIORITY = list(TERMS.keys())

MAX_PER_CHAPTER = 10

def is_safe_line(s):
    """Plain prose line (paragraph text)."""
    if not s.strip():
        return False
    return not s.lstrip().startswith(('#', '-', '*', '|', ':::', '<', '{', '>', '!', '---'))

def paragraph_end(lines, mask, i):
    """Return index AFTER the paragraph that starts at line i."""
    j = i
    while j + 1 < len(lines):
        if not lines[j + 1].strip() or not mask[j + 1]:
            break
        j += 1
    return j + 1

def safe_mask(lines):
    """Boolean per line: True = plain prose where an include may land nearby.
    Excludes code fences, YAML front matter, and fenced divs (callouts,
    tabsets — inserting ::: inside ::: would break the outer div)."""
    mask = [True] * len(lines)
    in_code = False
    in_yaml = False
    div_depth = 0
    for i, line in enumerate(lines):
        s = line.strip()
        if i == 0 and s == '---':
            in_yaml = True
            mask[i] = False
            continue
        if in_yaml:
            mask[i] = False
            if s == '---':
                in_yaml = False
            continue
        if s.startswith('```'):
            in_code = not in_code
            mask[i] = False
            continue
        if in_code:
            mask[i] = False
            continue
        if s.startswith(':::'):
            if '{' in s or s == ':::':
                if s == ':::':
                    div_depth = max(0, div_depth - 1)
                else:
                    div_depth += 1
            mask[i] = False
            continue
        if div_depth > 0:
            mask[i] = False
            continue
        if not is_safe_line(line):
            mask[i] = False
    return mask

def first_safe_index(lines, mask, pattern):
    rx = re.compile(pattern)
    for i, line in enumerate(lines):
        if mask[i] and rx.search(line):
            return i
    return None

total_includes = 0
fallback_used = {}

for path in sorted(glob.glob('capitulos/*.qmd')):
    if '_plantilla' in path:
        continue
    text = open(path, encoding='utf-8').read()
    used = [k for k in PRIORITY
            if re.search(TERMS[k], text)
            and os.path.exists(f'capitulos/_explicaciones/{k}.md')]
    # skip already-inserted
    used = [k for k in used if f'_explicaciones/{k}.md' not in text]
    used = used[:MAX_PER_CHAPTER]
    if not used:
        continue

    lines = text.split('\n')
    mask = safe_mask(lines)
    inserts = {}   # line-index-after-paragraph -> [slugs]
    fallback = []

    for slug in used:
        idx = first_safe_index(lines, mask, TERMS[slug])
        if idx is None:
            fallback.append(slug)
        else:
            pos = paragraph_end(lines, mask, idx)
            inserts.setdefault(pos, []).append(slug)

    # apply inserts bottom-up so indices stay valid
    # each include needs blank lines around it (block-level element)
    for pos in sorted(inserts, reverse=True):
        block = ['']
        for s in inserts[pos]:
            block.append(f'{{{{< include _explicaciones/{s}.md >}}}}')
            block.append('')
        lines[pos:pos] = block

    if fallback:
        # append before "## Lo que deberías saber hacer ahora" if present, else at EOF
        block = ['', '## Vocabulario técnico del capítulo', '']
        for s in fallback:
            block.append(f'{{{{< include _explicaciones/{s}.md >}}}}')
            block.append('')
        txt = '\n'.join(lines)
        marker = '## Lo que deberías saber hacer ahora'
        if marker in txt:
            txt = txt.replace(marker, '\n'.join(block) + '\n' + marker, 1)
            lines = txt.split('\n')
        else:
            lines += block
        fallback_used[path] = fallback

    out = '\n'.join(lines)
    open(path, 'w', encoding='utf-8').write(out)
    n = sum(len(v) for v in inserts.values()) + len(fallback)
    total_includes += n

print(f'inserted {total_includes} include calls')
for f, fb in fallback_used.items():
    print('fallback used in', f, '->', len(fb))
