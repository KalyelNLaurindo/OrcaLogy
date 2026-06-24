# TSK-50: Fix Cross-Platform CI Failures — Unicode & TUI on Linux

* **Owner / Assignee:** Kalyel N. Laurindo / Software Engineer
* **Estimated Effort:** 4 Hours
* **Story / Epic Reference:** CI Stability / Cross-Platform Quality
* **Development Methodology:** Investigação → Fix → Verificação em CI

## 📖 Description & Objectives

O pipeline do GitHub Actions executa corretamente em `ubuntu-latest`, mas dois problemas de cross-platform fazem com que os testes não representem a execução real do produto:

1. **Unicode / Encoding:** Caracteres especiais (emojis, símbolos ANSI, formatação UTF-8) usados nos outputs do CLI e nos widgets do Textual podem falhar com `UnicodeEncodeError` ou ser silenciosamente degradados quando o `LANG`/`LC_ALL` não está configurado como `UTF-8` no ambiente Linux do CI.

2. **Textual TUI em ambiente headless:** Os testes do TUI (`test_tui.py`) dependem de um terminal real. Em ambientes CI sem display, o Textual pode falhar ao detectar o tamanho do terminal (`shutil.get_terminal_size` retorna `(0, 0)`) ou lançar exceções de inicialização de driver.

Tarefas:
1. Auditar o workflow `ci.yml` e garantir que `PYTHONIOENCODING=utf-8` e `LANG=en_US.UTF-8` estejam definidos como variáveis de ambiente no job de testes.
2. Identificar todos os testes em `tests/test_tui.py` que requerem terminal interativo e aplicar `pytest.mark.skip` condicionado ao ambiente CI (`CI=true`) ou migrar para testes de snapshot com `textual.testing.App`.
3. Verificar se há caracteres hardcoded fora de arquivos de tradução que possam causar falha de encoding.
4. Validar que a suíte completa (`pytest`) passa no runner `ubuntu-latest` sem warnings de encoding.

## ✅ Definition of Ready (DoR)

* [x] CI pipeline configurado (TSK-34).
* [x] Suíte de testes completa existente com `test_tui.py` (96 testes).
* [x] Textual instalado como dependência de produção.

## 🏁 Definition of Done (DoD) & Acceptance Criteria

### BDD Scenarios (Gherkin Format):

```gherkin
Scenario: CI passa sem erros de encoding no Ubuntu
  Given o workflow do GitHub Actions executa em ubuntu-latest
  When o job de testes roda com PYTHONIOENCODING=utf-8 e LANG=en_US.UTF-8
  Then nenhum UnicodeEncodeError ou UnicodeDecodeError é lançado
  And todos os testes não-TUI passam com 100% de sucesso

Scenario: Testes de TUI não travam o runner headless
  Given o ambiente CI não possui terminal interativo
  When o pytest executa test_tui.py
  Then os testes TUI são pulados com @pytest.mark.skipif(CI) ou passam via Textual testing helpers
  And o runner não trava nem lança TimeoutError

Scenario: Outputs do CLI são compatíveis com Linux sem configuração manual
  Given um terminal Linux com encoding padrão
  When qualquer comando orca é executado (orca report, orca status, etc.)
  Then os caracteres Unicode são exibidos corretamente
  And nenhum símbolo é substituído por '?' ou causa crash
```

* [ ] **[CI - Encoding]:** `PYTHONIOENCODING=utf-8` e `LANG=en_US.UTF-8` adicionados ao `ci.yml`.
* [ ] **[CI - TUI]:** Testes dependentes de terminal real isolados com `skipif` ou refatorados com `textual.testing`.
* [ ] **[Verification]:** Pipeline verde no `ubuntu-latest` com zero falhas relacionadas a encoding ou TUI headless.
* [ ] **[Regression]:** Todos os 96+ testes existentes continuam passando localmente (Windows/macOS).
