#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ATCS Creator Intelligence v1.0
MVP local-first for Termux / Android. Uses Python standard library only.
"""
from __future__ import annotations

import argparse
import csv
import json
import re
import sys
from datetime import date, datetime
from pathlib import Path
from typing import Any

APP_NAME = "ATCS Creator Intelligence"
VERSION = "1.0.0"
ROOT = Path(__file__).resolve().parent
DATA_DIR = ROOT / "data"
OUTPUT_DIR = ROOT / "output"
CONFIG_FILE = DATA_DIR / "config.json"
IDEAS_FILE = DATA_DIR / "ideas.json"
METRICS_FILE = DATA_DIR / "metrics.csv"
COSTS_FILE = DATA_DIR / "costs.csv"

DEFAULT_CONFIG = {
    "channel_name": "Escola ATCS",
    "editorial_focus": "Educação tecnológica: Linux, Termux, automação e engenharia de sistemas",
    "audience": "Iniciantes em tecnologia, usuários Android, estudantes e desenvolvedores independentes",
    "primary_goal": "Validar audiência e construir receita sustentável para a Escola ATCS",
    "publishing_target": {"long_videos_per_week": 1, "shorts_per_week": 3},
    "disclaimer": "Resultados de audiência e receita não são garantidos. Validar toda afirmação técnica antes de publicar."
}

STARTER_IDEAS = [
    {
        "topic": "Como monitorar memória e processos no Android com Termux",
        "audience": "Iniciantes em Linux e usuários Android",
        "problem": "Entender quais informações do sistema podem ser consultadas sem root",
        "format": "long",
        "status": "idea",
        "notes": "Demonstrar free -h, uptime e ps -A; explicar limites de permissões."
    },
    {
        "topic": "Criando um monitor simples com Shell Script",
        "audience": "Iniciantes em automação",
        "problem": "Registrar métricas básicas sem copiar manualmente os resultados",
        "format": "long",
        "status": "idea",
        "notes": "Testar comandos no ambiente-alvo e evitar alegar monitoramento completo."
    },
    {
        "topic": "3 comandos Linux úteis no Android",
        "audience": "Iniciantes em Termux",
        "problem": "Aprender comandos práticos em menos de um minuto",
        "format": "short",
        "status": "idea",
        "notes": "Short derivado de demonstração real."
    },
    {
        "topic": "O que é Docker e para que serve?",
        "audience": "Iniciantes em desenvolvimento",
        "problem": "Entender imagem, container e porta HTTP",
        "format": "long",
        "status": "idea",
        "notes": "Usar exemplo simples e testar os comandos antes de gravar."
    }
]

def ensure_files() -> None:
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    if not CONFIG_FILE.exists():
        CONFIG_FILE.write_text(json.dumps(DEFAULT_CONFIG, ensure_ascii=False, indent=2), encoding="utf-8")
    if not IDEAS_FILE.exists():
        IDEAS_FILE.write_text(json.dumps(STARTER_IDEAS, ensure_ascii=False, indent=2), encoding="utf-8")
    for path, headers in [
        (METRICS_FILE, ["date", "video_title", "format", "impressions", "views", "ctr_percent", "avg_view_duration_seconds", "subscribers_gained", "link_clicks", "leads", "sales", "revenue_brl"]),
        (COSTS_FILE, ["date", "description", "category", "amount_brl"])
    ]:
        if not path.exists():
            with path.open("w", newline="", encoding="utf-8") as f:
                csv.writer(f).writerow(headers)

def load_json(path: Path) -> Any:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        print(f"Erro ao ler {path}: {exc}")
        return None

def slugify(text: str) -> str:
    text = text.lower().strip()
    replacements = {"á":"a","à":"a","â":"a","ã":"a","é":"e","ê":"e","í":"i","ó":"o","ô":"o","õ":"o","ú":"u","ç":"c"}
    for old, new in replacements.items():
        text = text.replace(old, new)
    text = re.sub(r"[^a-z0-9]+", "-", text).strip("-")
    return text[:70] or "conteudo-atcs"

def ask(prompt: str, default: str = "") -> str:
    suffix = f" [{default}]" if default else ""
    try:
        value = input(f"{prompt}{suffix}: ").strip()
    except (EOFError, KeyboardInterrupt):
        print()
        return default
    return value or default

def make_content_pack(topic: str, audience: str, problem: str, fmt: str = "long") -> str:
    config = load_json(CONFIG_FILE) or DEFAULT_CONFIG
    today = date.today().isoformat()
    is_short = fmt.lower() in ("short", "shorts", "vertical")
    if is_short:
        duration = "30–45 segundos"
        hook = f"Você quer entender {topic.lower()}? Veja esta demonstração rápida."
        script = f"""[0–3s | GANCHO]
Você quer entender {topic.lower()}? Veja esta demonstração rápida.

[3–10s | CONTEXTO]
O objetivo é ajudar {audience.lower()} a resolver esta questão: {problem.lower()}.

[10–30s | DEMONSTRAÇÃO]
Mostre a ferramenta ou procedimento real, em gravação de tela. Explique cada passo com frases curtas.
Não exiba credenciais, dados pessoais ou informações privadas.

[30–40s | EXPLICAÇÃO]
Resuma o que o resultado comprova e o que ele não comprova. Diferencie observação real de hipótese.

[40–45s | CTA]
Siga a Escola ATCS para acompanhar mais aulas práticas de tecnologia.
"""
        shorts = "Este conteúdo já está no formato Short. Faça uma versão alternativa com um gancho diferente e preserve a precisão técnica."
    else:
        duration = "5–8 minutos"
        hook = f"Hoje vamos resolver uma questão prática: {problem.rstrip('.')}."
        script = f"""[0:00–0:20 | GANCHO]
{hook}
Ao final, você saberá o que fazer, como verificar o resultado e quais limitações considerar.

[0:20–0:50 | CONTEXTO]
Este vídeo é voltado para {audience.lower()}.
Explique o problema e mostre rapidamente o resultado que será construído.

[0:50–1:30 | PREPARAÇÃO]
Mostre os requisitos, o ambiente e as versões relevantes. Informe se algum passo depende de permissões, internet ou instalação de pacotes.

[1:30–4:30 | DEMONSTRAÇÃO]
Execute cada etapa na tela, uma por vez.
Para cada comando ou procedimento:
1. Explique o que faz.
2. Execute em ambiente apropriado.
3. Mostre a saída real.
4. Explique como verificar se funcionou.
5. Registre erros e limitações relevantes.

[4:30–6:00 | INTERPRETAÇÃO]
Explique o resultado sem exagerar o que foi demonstrado. Separe fatos observados de hipóteses e planos futuros.

[6:00–7:00 | RESUMO E CTA]
Recapitule os passos e indique o próximo conteúdo relacionado.
Convide o espectador a se inscrever e comentar uma dúvida específica.
Só ofereça guias ou links que realmente estejam disponíveis.
"""
        shorts = f"""SHORT 1 — O problema em 30–40s
Gancho: “Você sabia que {problem.lower()}?”
Mostre uma etapa útil do vídeo principal e uma conclusão verificável.

SHORT 2 — Erro comum em 25–40s
Explique uma limitação ou interpretação equivocada relacionada a: {topic}.

SHORT 3 — Resultado em 20–35s
Mostre o antes/depois real, ou um resultado observável, e convide para o tutorial completo.
"""
    title1 = topic.strip().rstrip(".")
    title2 = f"Como resolver: {problem.rstrip('.')}"
    title3 = f"{topic.rstrip('.')} — tutorial prático para iniciantes"
    thumbnail = f"""CONCEITO DE THUMBNAIL
- Visual principal: captura real da ferramenta, terminal ou procedimento.
- Texto curto: “NA PRÁTICA” ou “PASSO A PASSO”.
- Contraste alto e poucos elementos.
- Não use números, resultados ou interfaces que não apareçam na demonstração.
"""
    description = f"""Neste tutorial da {config.get('channel_name', 'Escola ATCS')}, vamos abordar: {topic}.

Público: {audience}.
Objetivo: {problem}.

Você verá uma demonstração prática e as limitações importantes para interpretar o resultado corretamente.

📌 Capítulos sugeridos
00:00 Introdução
00:20 Contexto e requisitos
01:30 Demonstração
04:30 Como interpretar o resultado
06:00 Resumo

📚 Material complementar: adicionar somente quando estiver publicado.
💬 Comente qual tema de tecnologia você gostaria de ver no próximo episódio.

#EscolaATCS #Tecnologia #Linux #Programacao
"""
    quality = """CHECKLIST ANTES DE PUBLICAR
[ ] Todos os comandos foram testados no ambiente indicado.
[ ] A narração corresponde ao que aparece na tela.
[ ] As afirmações técnicas têm fontes confiáveis.
[ ] Nenhuma senha, token ou dado pessoal aparece.
[ ] A thumbnail não promete resultado não demonstrado.
[ ] Links, capítulos e chamadas para ação foram verificados.
[ ] O vídeo foi assistido do início ao fim antes da publicação.
"""
    return f"""# PACOTE DE PRODUÇÃO — {config.get('channel_name', 'Escola ATCS')}
Data de criação: {today}
Formato: {'Short' if is_short else 'Vídeo completo'}
Duração-alvo: {duration}

## 1. Objetivo
Ensinar algo verificável sobre “{topic}” e atender à necessidade: {problem}.

## 2. Público-alvo
{audience}

## 3. Títulos candidatos
1. {title1}
2. {title2}
3. {title3}

## 4. Gancho inicial
{hook}

## 5. Roteiro
{script}

## 6. Thumbnail
{thumbnail}

## 7. Descrição para YouTube
{description}

## 8. Conteúdos derivados
{shorts}

## 9. Fontes e validação
Adicionar links para documentação oficial ou fontes primárias consultadas durante a preparação. Não inventar referências.
Registrar aqui o ambiente testado, versão das ferramentas e limitações encontradas.

## 10. Hipótese comercial
Hipótese: o conteúdo atrai pessoas interessadas em aprender tecnologia.
Próximo passo: oferecer um material educativo gratuito somente quando estiver pronto e medir cliques voluntários.
Não considerar visualizações ou inscritos como receita garantida.

## 11. Métricas a registrar
Impressões, CTR, visualizações, duração média, inscritos ganhos, cliques, leads, vendas, receita e custos atribuíveis.

{quality}
"""

def generate_interactive() -> None:
    print("\n=== GERAR PACOTE DE CONTEÚDO ===")
    topic = ask("Tema do conteúdo", "Como monitorar memória e processos no Android com Termux")
    audience = ask("Público-alvo", "Iniciantes em Linux e usuários Android")
    problem = ask("Problema que o vídeo resolve", "Entender quais informações do sistema podem ser consultadas sem root")
    fmt = ask("Formato (long/short)", "long").lower()
    if fmt not in ("long", "short", "shorts", "vertical"):
        fmt = "long"
    content = make_content_pack(topic, audience, problem, fmt)
    filename = f"{date.today().isoformat()}_{slugify(topic)}.md"
    path = OUTPUT_DIR / filename
    path.write_text(content, encoding="utf-8")
    print(f"\nPacote criado: {path.relative_to(ROOT)}")
    print("Revise e teste as informações técnicas antes de gravar/publicar.")

def list_ideas() -> None:
    ideas = load_json(IDEAS_FILE) or []
    print("\n=== BANCO DE PAUTAS ===")
    if not ideas:
        print("Nenhuma pauta cadastrada.")
        return
    for i, idea in enumerate(ideas, 1):
        print(f"{i:02d}. [{idea.get('format','long')}] {idea.get('topic','(sem tema)')} — status: {idea.get('status','idea')}")
        print(f"    Público: {idea.get('audience','')}")
        print(f"    Problema: {idea.get('problem','')}")
    print(f"\nTotal: {len(ideas)} pautas")

def add_idea() -> None:
    ideas = load_json(IDEAS_FILE) or []
    topic = ask("Tema")
    if not topic:
        print("Tema vazio; cancelado.")
        return
    audience = ask("Público-alvo", "Iniciantes em tecnologia")
    problem = ask("Problema que resolve", "Aprender uma habilidade prática")
    fmt = ask("Formato (long/short)", "long").lower()
    notes = ask("Notas de produção", "")
    ideas.append({"topic": topic, "audience": audience, "problem": problem, "format": fmt, "status": "idea", "notes": notes})
    IDEAS_FILE.write_text(json.dumps(ideas, ensure_ascii=False, indent=2), encoding="utf-8")
    print("Pauta adicionada.")

def record_metrics() -> None:
    print("\n=== REGISTRAR MÉTRICAS ===")
    fields = [
        ("date", date.today().isoformat()),
        ("video_title", ask("Título do vídeo")),
        ("format", ask("Formato (long/short)", "long")),
        ("impressions", ask("Impressões", "0")),
        ("views", ask("Visualizações", "0")),
        ("ctr_percent", ask("CTR (%)", "0")),
        ("avg_view_duration_seconds", ask("Duração média assistida em segundos", "0")),
        ("subscribers_gained", ask("Inscritos ganhos", "0")),
        ("link_clicks", ask("Cliques em links", "0")),
        ("leads", ask("Leads/contatos voluntários", "0")),
        ("sales", ask("Vendas", "0")),
        ("revenue_brl", ask("Receita atribuída em R$", "0"))
    ]
    try:
        for idx in [3,4,5,6,7,8,9,10]:
            float(fields[idx][1].replace(",", "."))
        with METRICS_FILE.open("a", newline="", encoding="utf-8") as f:
            csv.writer(f).writerow([v for _, v in fields])
        print("Métricas registradas.")
    except ValueError:
        print("Valor numérico inválido. Nenhum registro foi salvo.")

def record_cost() -> None:
    print("\n=== REGISTRAR CUSTO ===")
    entry = [
        date.today().isoformat(),
        ask("Descrição"),
        ask("Categoria", "software"),
        ask("Valor em R$", "0").replace(",", ".")
    ]
    try:
        amount = float(entry[3])
        if amount < 0:
            raise ValueError
        entry[3] = f"{amount:.2f}"
        with COSTS_FILE.open("a", newline="", encoding="utf-8") as f:
            csv.writer(f).writerow(entry)
        print("Custo registrado.")
    except ValueError:
        print("Valor inválido. Use um número igual ou maior que zero.")

def report() -> None:
    def sum_csv(path: Path, field: str) -> float:
        total = 0.0
        try:
            with path.open(newline="", encoding="utf-8") as f:
                for row in csv.DictReader(f):
                    try:
                        total += float((row.get(field) or "0").replace(",", "."))
                    except ValueError:
                        pass
        except OSError:
            pass
        return total
    views = sum_csv(METRICS_FILE, "views")
    sales = sum_csv(METRICS_FILE, "sales")
    revenue = sum_csv(METRICS_FILE, "revenue_brl")
    costs = sum_csv(COSTS_FILE, "amount_brl")
    net = revenue - costs
    print("\n=== RELATÓRIO SIMPLES ===")
    print(f"Visualizações registradas: {views:.0f}")
    print(f"Vendas registradas: {sales:.0f}")
    print(f"Receita atribuída: R$ {revenue:.2f}")
    print(f"Custos registrados: R$ {costs:.2f}")
    print(f"Saldo simples (receita - custos): R$ {net:.2f}")
    print("Nota: valores dependem dos registros inseridos e não incluem custos ou receitas omitidos.")
    if views > 0:
        print(f"Vendas por 1.000 visualizações registradas: {sales / views * 1000:.2f}")
    else:
        print("Ainda não há visualizações registradas para calcular a taxa.")

def show_menu() -> None:
    while True:
        print(f"""
=== {APP_NAME} v{VERSION} ===
1. Gerar pacote de conteúdo
2. Listar banco de pautas
3. Adicionar pauta
4. Registrar métricas de vídeo
5. Registrar custo
6. Ver relatório de receita
0. Sair
""")
        choice = ask("Escolha")
        if choice == "1":
            generate_interactive()
        elif choice == "2":
            list_ideas()
        elif choice == "3":
            add_idea()
        elif choice == "4":
            record_metrics()
        elif choice == "5":
            record_cost()
        elif choice == "6":
            report()
        elif choice == "0":
            print("ATCS Creator Intelligence encerrado.")
            return
        else:
            print("Opção inválida.")

def main() -> int:
    ensure_files()
    parser = argparse.ArgumentParser(description=APP_NAME)
    parser.add_argument("--generate", metavar="TEMA", help="Gera pacote Markdown usando o tema informado")
    parser.add_argument("--format", choices=["long", "short"], default="long", help="Formato do pacote")
    parser.add_argument("--audience", default="Iniciantes em tecnologia", help="Público-alvo")
    parser.add_argument("--problem", default="Aprender uma habilidade prática", help="Problema que o conteúdo resolve")
    parser.add_argument("--ideas", action="store_true", help="Lista as pautas cadastradas")
    parser.add_argument("--report", action="store_true", help="Mostra relatório de métricas e custos")
    args = parser.parse_args()

    if args.generate:
        content = make_content_pack(args.generate, args.audience, args.problem, args.format)
        filename = f"{date.today().isoformat()}_{slugify(args.generate)}.md"
        path = OUTPUT_DIR / filename
        path.write_text(content, encoding="utf-8")
        print(f"Pacote criado: {path}")
        return 0
    if args.ideas:
        list_ideas()
        return 0
    if args.report:
        report()
        return 0
    show_menu()
    return 0

if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except BrokenPipeError:
        raise SystemExit(0)
