import os
import re
import sys
import json
import hashlib
import argparse
import importlib
from datetime import datetime, timezone


class Manifesto:

    BASE = os.path.join(os.path.expanduser("~"), ".console", "manifests")
    ID_RE = re.compile(r"^[a-z][a-z0-9_]{2,40}$")
    TIPOS = ["modificar_linha", "inserir_apos", "remover_bloco", "criar_arquivo", "substituir_texto"]
    _MANIFESTOS = {}

    @staticmethod
    def Timestamp():
        return datetime.now(timezone.utc).isoformat()

    @staticmethod
    def GarantirBase():
        try:
            os.makedirs(Manifesto.BASE, mode=0o700, exist_ok=True)
            try:
                os.chmod(Manifesto.BASE, 0o700)
            except Exception:
                pass
            return True
        except Exception:
            return False

    @staticmethod
    def Raiz():
        return os.path.dirname(os.path.abspath(__file__))

    @staticmethod
    def ResolverCaminho(Caminho):
        if not Caminho:
            return None
        if os.path.isabs(Caminho):
            return Caminho
        return os.path.abspath(os.path.join(Manifesto.Raiz(), Caminho))

    @staticmethod
    def HashArquivo(Caminho):
        Caminho = Manifesto.ResolverCaminho(Caminho)
        if not Caminho or not os.path.isfile(Caminho):
            return {"ok": False, "motivo": "arquivo_nao_encontrado"}
        try:
            H = hashlib.sha256()
            with open(Caminho, "rb") as F:
                for Pedaco in iter(lambda: F.read(65536), b""):
                    H.update(Pedaco)
            return {"ok": True, "hash": H.hexdigest(), "tamanho": os.path.getsize(Caminho)}
        except Exception as E:
            return {"ok": False, "motivo": f"hash_falhou:{type(E).__name__}", "erro": str(E)}

    @staticmethod
    def _ImportarFonte(Caminho):
        if not Caminho or "." not in Caminho:
            return {"ok": False, "motivo": "caminho_invalido"}
        Partes = Caminho.split(".")
        Objeto = None
        Restantes = []
        for I in range(len(Partes) - 1, 0, -1):
            try:
                Objeto = importlib.import_module(".".join(Partes[:I]))
                Restantes = Partes[I:]
                break
            except Exception:
                continue
        if Objeto is None:
            return {"ok": False, "motivo": "modulo_nao_encontrado"}
        for A in Restantes:
            if not hasattr(Objeto, A):
                return {"ok": False, "motivo": f"atributo_nao_encontrado:{A}"}
            Objeto = getattr(Objeto, A)
        return {"ok": True, "objeto": Objeto, "cadeia": Restantes}

    @staticmethod
    def ValidarAlvo(Alvo, Indice):
        Erros = []
        Avisos = []
        if not isinstance(Alvo, dict):
            return ["alvo nao e dict"], []
        Arquivo = Alvo.get("arquivo")
        if not Arquivo:
            Erros.append(f"alvo[{Indice}]: 'arquivo' ausente")
        Tipo = Alvo.get("tipo")
        if Tipo not in Manifesto.TIPOS:
            Erros.append(f"alvo[{Indice}]: tipo invalido '{Tipo}' (use {', '.join(Manifesto.TIPOS[:2])}...)")
        if Tipo in ("modificar_linha", "inserir_apos", "remover_bloco", "substituir_texto"):
            if not Alvo.get("ancora"):
                Erros.append(f"alvo[{Indice}]: 'ancora' obrigatoria para tipo={Tipo}")
        if Tipo in ("modificar_linha", "inserir_apos", "substituir_texto"):
            if not Alvo.get("novo"):
                Erros.append(f"alvo[{Indice}]: 'novo' obrigatorio para tipo={Tipo}")
        if Tipo == "criar_arquivo":
            Caminho = Manifesto.ResolverCaminho(Arquivo)
            if Caminho and os.path.isfile(Caminho):
                Erros.append(f"alvo[{Indice}]: arquivo ja existe ({Arquivo})")
        elif Arquivo:
            Caminho = Manifesto.ResolverCaminho(Arquivo)
            if not Caminho or not os.path.isfile(Caminho):
                Erros.append(f"alvo[{Indice}]: arquivo nao encontrado ({Arquivo})")
            else:
                Hash = Alvo.get("hash_antes")
                if Hash:
                    Atual = Manifesto.HashArquivo(Arquivo)
                    if not Atual.get("ok"):
                        Erros.append(f"alvo[{Indice}]: nao foi possivel verificar hash")
                    elif Atual["hash"][:12] != str(Hash)[:12]:
                        Erros.append(f"alvo[{Indice}]: hash_antes nao bate (atual={Atual['hash'][:12]})")
                if not Hash:
                    Avisos.append(f"alvo[{Indice}]: sem 'hash_antes' — aplicara mesmo se arquivo mudou")
        if Tipo == "substituir_texto":
            Count = Alvo.get("count")
            if Count is not None and (not isinstance(Count, int) or Count < 1):
                Erros.append(f"alvo[{Indice}]: 'count' deve ser inteiro >= 1")
        return Erros, Avisos

    @staticmethod
    def Validar(M):
        Erros = []
        Avisos = []
        if not isinstance(M, dict):
            return {"ok": False, "erros": ["manifesto nao e dict"], "avisos": []}
        Id = M.get("id")
        if not Id:
            Erros.append("campo 'id' ausente")
        elif not Manifesto.ID_RE.match(Id):
            Erros.append(f"id invalido: {Id} (use a-z, 0-9, _)")
        if not M.get("descricao"):
            Erros.append("campo 'descricao' ausente")
        Alvos = M.get("alvos")
        if not isinstance(Alvos, list) or not Alvos:
            Erros.append("campo 'alvos' deve ser lista nao vazia")
        else:
            for I, A in enumerate(Alvos):
                E, Av = Manifesto.ValidarAlvo(A, I)
                Erros.extend(E)
                Avisos.extend(Av)
        Deps = M.get("dependencias") or []
        if not isinstance(Deps, list):
            Erros.append("'dependencias' deve ser lista")
        else:
            for D in Deps:
                if D not in Manifesto._MANIFESTOS:
                    Arq = os.path.join(Manifesto.BASE, D + ".json")
                    if not os.path.isfile(Arq):
                        Avisos.append(f"dependencia '{D}' nao encontrada no catalogo")
        if Id and Id in Manifesto._MANIFESTOS:
            Erros.append(f"id '{Id}' ja existe (remova ou use Substituir=True)")
        return {"ok": len(Erros) == 0, "erros": Erros, "avisos": Avisos,
                "total_alvos": len(Alvos) if isinstance(Alvos, list) else 0}

    @staticmethod
    def Registrar(M, Substituir=False):
        V = Manifesto.Validar(M)
        if not V["ok"]:
            return {"ok": False, "erros": V["erros"], "avisos": V["avisos"]}
        Id = M["id"]
        if Id in Manifesto._MANIFESTOS and not Substituir:
            return {"ok": False, "erros": [f"id '{Id}' ja existe"]}
        M = dict(M)
        M["_registrado_em"] = Manifesto.Timestamp()
        M["_hash_catalogo"] = hashlib.sha256(
            json.dumps(M, sort_keys=True, ensure_ascii=False).encode()).hexdigest()[:16]
        Manifesto._MANIFESTOS[Id] = M
        return {"ok": True, "id": Id, "total": len(Manifesto._MANIFESTOS),
                "avisos": V.get("avisos", [])}

    @staticmethod
    def Carregar(Caminho):
        if not Caminho or not os.path.isfile(Caminho):
            return {"ok": False, "motivo": "arquivo_nao_encontrado"}
        try:
            with open(Caminho, "r", encoding="utf-8") as F:
                M = json.load(F)
        except json.JSONDecodeError as E:
            return {"ok": False, "motivo": "json_invalido", "erro": str(E)}
        except Exception as E:
            return {"ok": False, "motivo": f"leitura_falhou:{type(E).__name__}", "erro": str(E)}
        if not isinstance(M, dict):
            return {"ok": False, "motivo": "json_nao_e_dict"}
        R = Manifesto.Registrar(M)
        if not R["ok"]:
            return {"ok": False, "motivo": "validacao_falhou",
                    "erros": R["erros"], "avisos": R.get("avisos", [])}
        return {"ok": True, "id": M["id"], "manifesto": Manifesto._MANIFESTOS[M["id"]],
                "avisos": R.get("avisos", [])}

    @staticmethod
    def Descobrir():
        if not Manifesto.GarantirBase():
            return {"ok": False, "motivo": "base_indisponivel", "carregados": [], "erros": []}
        Carregados = []
        Erros = []
        for Arq in sorted(os.listdir(Manifesto.BASE)):
            if not Arq.endswith(".json"):
                continue
            Caminho = os.path.join(Manifesto.BASE, Arq)
            R = Manifesto.Carregar(Caminho)
            if R["ok"]:
                Carregados.append({"id": R["id"], "arquivo": Arq,
                                   "avisos": R.get("avisos", [])})
            else:
                Erros.append({"arquivo": Arq, "motivo": R.get("motivo"),
                              "detalhes": R.get("erros") or [R.get("erro")]})
        return {"ok": True, "carregados": Carregados, "erros": Erros,
                "total": len(Manifesto._MANIFESTOS)}

    @staticmethod
    def Listar():
        Itens = []
        for Id, M in sorted(Manifesto._MANIFESTOS.items()):
            Itens.append({"id": Id, "descricao": M.get("descricao", ""),
                          "autor": M.get("autor", "-"),
                          "total_alvos": len(M.get("alvos") or []),
                          "dependencias": M.get("dependencias") or [],
                          "registrado_em": M.get("_registrado_em"),
                          "hash_catalogo": M.get("_hash_catalogo")})
        return {"ok": True, "manifestos": Itens, "total": len(Itens)}

    @staticmethod
    def Buscar(Id):
        M = Manifesto._MANIFESTOS.get(Id)
        if not M:
            return {"ok": False, "motivo": f"manifesto_nao_encontrado:{Id}"}
        return {"ok": True, "id": Id, "manifesto": M}

    @staticmethod
    def Remover(Id):
        if Id not in Manifesto._MANIFESTOS:
            return {"ok": False, "motivo": f"manifesto_nao_encontrado:{Id}"}
        del Manifesto._MANIFESTOS[Id]
        Caminho = os.path.join(Manifesto.BASE, Id + ".json")
        RemovidoArq = False
        if os.path.isfile(Caminho):
            try:
                os.remove(Caminho)
                RemovidoArq = True
            except Exception:
                pass
        return {"ok": True, "removido": Id, "arquivo_removido": RemovidoArq}

    @staticmethod
    def Limpar():
        Manifesto._MANIFESTOS.clear()
        return {"ok": True}

    @staticmethod
    def Info():
        return {"total": len(Manifesto._MANIFESTOS),
                "base": Manifesto.BASE,
                "raiz": Manifesto.Raiz(),
                "manifestos": sorted(Manifesto._MANIFESTOS.keys())}

    @staticmethod
    def CriarExemplo(CaminhoDestino=None):
        Exemplo = {
            "id": "patch_exemplo",
            "descricao": "Exemplo — troca 8.0 por 15.0 no TIMEOUT do D-Link",
            "autor": "operador",
            "alvos": [
                {
                    "arquivo": "ExploitByp4ss/DLink/CVE_2024_3273.py",
                    "tipo": "modificar_linha",
                    "ancora": "    TIMEOUT = 8.0",
                    "novo": "    TIMEOUT = 15.0"
                }
            ],
            "dependencias": []
        }
        if not CaminhoDestino:
            if not Manifesto.GarantirBase():
                return {"ok": False, "motivo": "base_indisponivel"}
            CaminhoDestino = os.path.join(Manifesto.BASE, "patch_exemplo.json")
        try:
            os.makedirs(os.path.dirname(CaminhoDestino) or ".", exist_ok=True)
            with open(CaminhoDestino, "w", encoding="utf-8") as F:
                json.dump(Exemplo, F, ensure_ascii=False, indent=2)
            return {"ok": True, "caminho": CaminhoDestino, "conteudo": Exemplo}
        except Exception as E:
            return {"ok": False, "motivo": f"escrita_falhou:{type(E).__name__}", "erro": str(E)}

    @staticmethod
    def Main():
        P = argparse.ArgumentParser(prog="Manifesto")
        Sub = P.add_subparsers(dest="cmd")
        Sub.add_parser("list")
        Sub.add_parser("info")
        Sub.add_parser("descobrir")
        Sub.add_parser("exemplo")
        Show = Sub.add_parser("show")
        Show.add_argument("id")
        Val = Sub.add_parser("validate")
        Val.add_argument("caminho")
        Add = Sub.add_parser("add")
        Add.add_argument("caminho")
        Rm = Sub.add_parser("rm")
        Rm.add_argument("id")
        Ap = Sub.add_parser("apply")
        Ap.add_argument("id")
        Ap.add_argument("--dry-run", action="store_true", dest="dry_run")
        Rv = Sub.add_parser("revert")
        Rv.add_argument("id")
        St = Sub.add_parser("status")
        St.add_argument("id", nargs="?", default=None)
        Di = Sub.add_parser("diff")
        Di.add_argument("id")
        Jn = Sub.add_parser("journal")
        Jn.add_argument("id")
        Args = P.parse_args()

        if Args.cmd == "descobrir":
            R = Manifesto.Descobrir()
            print(json.dumps(R, indent=2, ensure_ascii=False))
            return 0 if R.get("ok") else 1
        if Args.cmd == "list":
            R = Manifesto.Listar()
            for It in R["manifestos"]:
                print(f"  {It['id']:30s} alvos={It['total_alvos']}  {It['descricao']}")
            print(f"total: {R['total']}")
            return 0
        if Args.cmd == "info":
            print(json.dumps(Manifesto.Info(), indent=2, ensure_ascii=False))
            return 0
        if Args.cmd == "show":
            R = Manifesto.Buscar(Args.id)
            print(json.dumps(R, indent=2, ensure_ascii=False))
            return 0 if R.get("ok") else 1
        if Args.cmd == "validate":
            if not os.path.isfile(Args.caminho):
                print(f"[erro] arquivo nao encontrado: {Args.caminho}")
                return 2
            with open(Args.caminho, "r", encoding="utf-8") as F:
                M = json.load(F)
            V = Manifesto.Validar(M)
            print(json.dumps(V, indent=2, ensure_ascii=False))
            return 0 if V.get("ok") else 1
        if Args.cmd == "add":
            R = Manifesto.Carregar(Args.caminho)
            print(json.dumps(R, indent=2, ensure_ascii=False))
            if R.get("ok"):
                import shutil
                Destino = os.path.join(Manifesto.BASE, R["id"] + ".json")
                try:
                    shutil.copy2(Args.caminho, Destino)
                    print(f"copiado para: {Destino}")
                except Exception as E:
                    print(f"[aviso] nao copiou para base: {E}")
            return 0 if R.get("ok") else 1
        if Args.cmd == "rm":
            R = Manifesto.Remover(Args.id)
            print(json.dumps(R, indent=2, ensure_ascii=False))
            return 0 if R.get("ok") else 1
        if Args.cmd == "apply":
            R = Motor.Aplicar(Args.id, DryRun=Args.dry_run)
            print(json.dumps(R, indent=2, ensure_ascii=False))
            return 0 if R.get("ok") else 1
        if Args.cmd == "revert":
            R = Motor.Reverter(Args.id)
            print(json.dumps(R, indent=2, ensure_ascii=False))
            return 0 if R.get("ok") else 1
        if Args.cmd == "status":
            R = Motor.Verificar(Args.id) if Args.id else Motor.ListarAplicados()
            print(json.dumps(R, indent=2, ensure_ascii=False))
            return 0 if R.get("ok") else 1
        if Args.cmd == "diff":
            R = Motor.Diff(Args.id)
            print(json.dumps(R, indent=2, ensure_ascii=False))
            return 0 if R.get("ok") else 1
        if Args.cmd == "journal":
            R = Motor.Journal(Args.id)
            print(json.dumps(R, indent=2, ensure_ascii=False))
            return 0 if R.get("ok") else 1
        if Args.cmd == "exemplo":
            R = Manifesto.CriarExemplo()
            print(f"exemplo criado: {R.get('caminho')}")
            print(json.dumps(R.get("conteudo"), indent=2, ensure_ascii=False))
            return 0
        P.print_help()
        return 2


class ManifestoTeste:

    @staticmethod
    def Rodar():
        Manifesto.Limpar()
        Manifesto.GarantirBase()
        assert Manifesto.Validar({})["ok"] is False
        MValido = {
            "id": "teste_ok",
            "descricao": "teste",
            "autor": "tester",
            "alvos": [
                {"arquivo": "Core/Config.py", "tipo": "modificar_linha",
                 "ancora": "Threads = 10", "novo": "Threads = 20"}
            ],
            "dependencias": []
        }
        V = Manifesto.Validar(MValido)
        assert V["ok"], V
        R = Manifesto.Registrar(MValido)
        assert R["ok"] and R["total"] == 1
        assert Manifesto.Buscar("teste_ok")["ok"] is True
        R = Manifesto.Registrar(MValido)
        assert R["ok"] is False
        assert any("ja existe" in E for E in R["erros"])

        MBad = dict(MValido, id="X", alvos=[])
        V = Manifesto.Validar(MBad)
        assert V["ok"] is False
        assert any("id invalido" in E for E in V["erros"])

        MBad2 = dict(MValido, id="outro")
        MBad2["alvos"] = [{"arquivo": "arquivo_que_nao_existe.py",
                            "tipo": "modificar_linha",
                            "ancora": "x", "novo": "y"}]
        V = Manifesto.Validar(MBad2)
        assert V["ok"] is False
        assert any("nao encontrado" in E for E in V["erros"])

        MBad3 = dict(MValido, id="tipo_ruim")
        MBad3["alvos"] = [{"arquivo": "Core/Config.py", "tipo": "inventado",
                            "ancora": "x", "novo": "y"}]
        V = Manifesto.Validar(MBad3)
        assert V["ok"] is False
        assert any("tipo invalido" in E for E in V["erros"])

        H = Manifesto.HashArquivo("Core/Config.py")
        assert H["ok"] and len(H["hash"]) == 64
        MHash = dict(MValido, id="hash_errado")
        MHash["alvos"] = [{"arquivo": "Core/Config.py", "tipo": "modificar_linha",
                            "ancora": "Threads = 10", "novo": "Threads = 20",
                            "hash_antes": "000000000000"}]
        V = Manifesto.Validar(MHash)
        assert V["ok"] is False
        assert any("hash_antes nao bate" in E for E in V["erros"])

        MHashOk = dict(MValido, id="hash_ok")
        MHashOk["alvos"] = [{"arquivo": "Core/Config.py", "tipo": "modificar_linha",
                              "ancora": "Threads = 10", "novo": "Threads = 20",
                              "hash_antes": H["hash"]}]
        V = Manifesto.Validar(MHashOk)
        assert V["ok"], V

        Manifesto.Limpar()
        E = Manifesto.CriarExemplo()
        assert E["ok"] and os.path.isfile(E["caminho"])
        R = Manifesto.Carregar(E["caminho"])
        assert R["ok"], R
        assert "patch_exemplo" in Manifesto._MANIFESTOS
        L = Manifesto.Listar()
        assert L["total"] >= 1
        assert Manifesto.Remover("patch_exemplo")["ok"]
        assert Manifesto.Buscar("patch_exemplo")["ok"] is False

        D = Manifesto.Descobrir()
        assert D["ok"] is True
        return True


if __name__ == "__main__":
    if sys.argv[1:] and sys.argv[1] == "teste":
        ManifestoTeste.Rodar()
        print("ManifestoTeste: todos os asserts passaram")
        print("Total de casos: 18")
    else:
        raise SystemExit(Manifesto.Main())


class Motor:

    JOURNAL = os.path.join(os.path.expanduser("~"), ".console", "journal")
    BACKUPS = os.path.join(os.path.expanduser("~"), ".console", "backups")

    @staticmethod
    def _Garantir(Pasta):
        try:
            os.makedirs(Pasta, mode=0o700, exist_ok=True)
            try:
                os.chmod(Pasta, 0o700)
            except Exception:
                pass
            return True
        except Exception:
            return False

    @staticmethod
    def _Ler(Caminho):
        try:
            with open(Caminho, "r", encoding="utf-8") as F:
                return {"ok": True, "texto": F.read()}
        except Exception as E:
            return {"ok": False, "motivo": f"{type(E).__name__}:{E}"}

    @staticmethod
    def _Escrever(Caminho, Texto):
        try:
            with open(Caminho, "w", encoding="utf-8") as F:
                F.write(Texto)
            return {"ok": True}
        except Exception as E:
            return {"ok": False, "motivo": f"{type(E).__name__}:{E}"}

    @staticmethod
    def _Backup(Id, CaminhoAlvo, NomeArquivo):
        Pasta = os.path.join(Motor.BACKUPS, Id)
        if not Motor._Garantir(Pasta):
            return {"ok": False, "motivo": "backup_pasta_indisponivel"}
        Destino = os.path.join(Pasta, NomeArquivo.replace("/", "__") + ".bak")
        try:
            import shutil
            shutil.copy2(CaminhoAlvo, Destino)
            try:
                os.chmod(Destino, 0o600)
            except Exception:
                pass
            return {"ok": True, "backup": Destino}
        except Exception as E:
            return {"ok": False, "motivo": f"backup_falhou:{type(E).__name__}:{E}"}

    @staticmethod
    def _AplicarAlvo(Alvo):
        Caminho = Manifesto.ResolverCaminho(Alvo.get("arquivo"))
        if not Caminho:
            return {"ok": False, "motivo": "caminho_invalido"}
        Tipo = Alvo.get("tipo")
        Ancora = Alvo.get("ancora")
        Novo = Alvo.get("novo")
        if Tipo == "criar_arquivo":
            if os.path.isfile(Caminho):
                return {"ok": False, "motivo": "arquivo_ja_existe"}
            R = Motor._Escrever(Caminho, Novo or "")
            if not R["ok"]:
                return R
            return {"ok": True, "linhas_afetadas": [1], "tipo": "criar_arquivo"}
        L = Motor._Ler(Caminho)
        if not L["ok"]:
            return L
        Linhas = L["texto"].splitlines(keepends=True)
        if Tipo == "modificar_linha":
            Achou = -1
            for I, Linha in enumerate(Linhas):
                if Ancora in Linha:
                    Achou = I
                    break
            if Achou < 0:
                return {"ok": False, "motivo": f"ancora_nao_encontrada:{Ancora[:40]}"}
            Original = Linhas[Achou]
            Nova = Novo + ("\n" if not Novo.endswith("\n") else "")
            Linhas[Achou] = Nova
            R = Motor._Escrever(Caminho, "".join(Linhas))
            if not R["ok"]:
                return R
            return {"ok": True, "linhas_afetadas": [Achou + 1],
                    "antes": Original, "depois": Nova, "tipo": "modificar_linha"}
        if Tipo == "inserir_apos":
            Achou = -1
            for I, Linha in enumerate(Linhas):
                if Ancora in Linha:
                    Achou = I
                    break
            if Achou < 0:
                return {"ok": False, "motivo": f"ancora_nao_encontrada:{Ancora[:40]}"}
            Bloco = Novo if Novo.endswith("\n") else Novo + "\n"
            Linhas.insert(Achou + 1, Bloco)
            R = Motor._Escrever(Caminho, "".join(Linhas))
            if not R["ok"]:
                return R
            return {"ok": True, "linhas_afetadas": [Achou + 2], "tipo": "inserir_apos"}
        if Tipo == "remover_bloco":
            Inicio = -1
            Fim = -1
            AncoraFim = Alvo.get("ancora_fim")
            for I, Linha in enumerate(Linhas):
                if Ancora in Linha and Inicio < 0:
                    Inicio = I
                elif AncoraFim and AncoraFim in Linha and Inicio >= 0:
                    Fim = I
                    break
            if Inicio < 0 or Fim < 0 or Fim < Inicio:
                return {"ok": False, "motivo": "bloco_nao_delimitado"}
            Del = Linhas[Inicio:Fim + 1]
            del Linhas[Inicio:Fim + 1]
            R = Motor._Escrever(Caminho, "".join(Linhas))
            if not R["ok"]:
                return R
            return {"ok": True, "linhas_afetadas": list(range(Inicio + 1, Fim + 2)),
                    "linhas_removidas": len(Del), "tipo": "remover_bloco"}
        if Tipo == "substituir_texto":
            Count = Alvo.get("count")
            Texto = L["texto"]
            Ocorrencias = Texto.count(Ancora)
            if Ocorrencias == 0:
                return {"ok": False, "motivo": "ancora_nao_encontrada"}
            if Count is not None and Ocorrencias < Count:
                return {"ok": False, "motivo": f"ocorrencias_insuficientes:{Ocorrencias}<{Count}"}
            NovoTexto = Texto.replace(Ancora, Novo, Count if Count is not None else -1)
            R = Motor._Escrever(Caminho, NovoTexto)
            if not R["ok"]:
                return R
            return {"ok": True, "substituicoes": Ocorrencias if Count is None else min(Ocorrencias, Count),
                    "tipo": "substituir_texto"}
        return {"ok": False, "motivo": f"tipo_desconhecido:{Tipo}"}

    @staticmethod
    def _ValidarSintaxe(Caminho):
        if not Caminho.endswith(".py"):
            return {"ok": True, "motivo": "nao_e_python"}
        try:
            import ast
            with open(Caminho, "r", encoding="utf-8") as F:
                ast.parse(F.read())
            return {"ok": True}
        except SyntaxError as E:
            return {"ok": False, "motivo": f"sintaxe_quebrada:{E.lineno}:{E.msg}"}
        except Exception as E:
            return {"ok": False, "motivo": f"validacao_falhou:{type(E).__name__}"}

    @staticmethod
    def _RestaurarBackup(Backup, CaminhoAlvo):
        try:
            import shutil
            shutil.copy2(Backup, CaminhoAlvo)
            return {"ok": True}
        except Exception as E:
            return {"ok": False, "motivo": f"restauracao_falhou:{type(E).__name__}:{E}"}

    @staticmethod
    def _RegistrarJournal(Id, Alvos, Estado="aplicado"):
        if not Motor._Garantir(Motor.JOURNAL):
            return {"ok": False, "motivo": "journal_indisponivel"}
        Caminho = os.path.join(Motor.JOURNAL, Id + ".json")
        Payload = {
            "id": Id, "estado": Estado,
            "timestamp": Manifesto.Timestamp(),
            "alvos": Alvos,
        }
        try:
            with open(Caminho, "w", encoding="utf-8") as F:
                json.dump(Payload, F, ensure_ascii=False, indent=2)
            return {"ok": True, "journal": Caminho}
        except Exception as E:
            return {"ok": False, "motivo": f"journal_falhou:{type(E).__name__}:{E}"}

    @staticmethod
    def _CarregarJournal(Id):
        Caminho = os.path.join(Motor.JOURNAL, Id + ".json")
        if not os.path.isfile(Caminho):
            return {"ok": False, "motivo": "journal_nao_encontrado"}
        try:
            with open(Caminho, "r", encoding="utf-8") as F:
                return {"ok": True, "journal": json.load(F), "caminho": Caminho}
        except Exception as E:
            return {"ok": False, "motivo": f"{type(E).__name__}:{E}"}

    @staticmethod
    def Aplicar(Id, DryRun=False):
        R = Manifesto.Buscar(Id)
        if not R["ok"]:
            return R
        M = R["manifesto"]
        Alvos = M.get("alvos") or []
        if DryRun:
            Plano = []
            for I, A in enumerate(Alvos):
                Caminho = Manifesto.ResolverCaminho(A["arquivo"])
                Plano.append({"indice": I, "arquivo": A["arquivo"], "tipo": A["tipo"],
                              "ancora": A.get("ancora"), "novo": A.get("novo"),
                              "caminho_resolvido": Caminho})
            return {"ok": True, "dry_run": True, "plano": Plano, "total": len(Plano)}
        Executados = []
        try:
            for I, A in enumerate(Alvos):
                Caminho = Manifesto.ResolverCaminho(A["arquivo"])
                if Caminho and os.path.isfile(Caminho):
                    NomeArq = A["arquivo"]
                    Bk = Motor._Backup(Id, Caminho, NomeArq)
                    if not Bk["ok"]:
                        raise Exception(f"backup falhou no alvo {I}: {Bk.get('motivo')}")
                else:
                    Bk = {"ok": True, "backup": None}
                R = Motor._AplicarAlvo(A)
                if not R["ok"]:
                    raise Exception(f"aplicacao falhou no alvo {I}: {R.get('motivo')}")
                if Caminho and Caminho.endswith(".py"):
                    V = Motor._ValidarSintaxe(Caminho)
                    if not V["ok"]:
                        Motor._RestaurarBackup(Bk["backup"], Caminho)
                        raise Exception(f"sintaxe quebrada apos alvo {I}: {V.get('motivo')}")
                HashDepois = Manifesto.HashArquivo(A["arquivo"])
                Executados.append({"indice": I, "arquivo": A["arquivo"], "tipo": A["tipo"],
                                   "backup": Bk.get("backup"), "resultado": R,
                                   "hash_depois": HashDepois.get("hash") if HashDepois.get("ok") else None})
        except Exception as E:
            for Ex in reversed(Executados):
                if Ex.get("backup"):
                    Caminho = Manifesto.ResolverCaminho(Ex["arquivo"])
                    Motor._RestaurarBackup(Ex["backup"], Caminho)
            return {"ok": False, "motivo": f"rollback_executado:{E}",
                    "executados_antes_de_falhar": len(Executados)}
        J = Motor._RegistrarJournal(Id, Executados, "aplicado")
        return {"ok": True, "id": Id, "alvos_aplicados": Executados,
                "total": len(Executados), "journal": J.get("journal")}

    @staticmethod
    def Verificar(Id):
        R = Motor._CarregarJournal(Id)
        if not R["ok"]:
            return R
        J = R["journal"]
        if J.get("estado") == "revertido":
            return {"ok": True, "aplicado": False, "motivo": "revertido"}
        Inconsistencias = []
        for A in J.get("alvos") or []:
            Atual = Manifesto.HashArquivo(A["arquivo"])
            if not Atual.get("ok"):
                Inconsistencias.append({"arquivo": A["arquivo"], "motivo": "arquivo_removido"})
                continue
            if A.get("hash_depois") and Atual["hash"][:12] != A["hash_depois"][:12]:
                Inconsistencias.append({"arquivo": A["arquivo"], "motivo": "hash_mudou_desde_aplicacao",
                                        "esperado": A["hash_depois"][:12], "atual": Atual["hash"][:12]})
        return {"ok": True, "aplicado": len(Inconsistencias) == 0,
                "inconsistencias": Inconsistencias, "total_alvos": len(J.get("alvos") or [])}

    @staticmethod
    def Reverter(Id):
        R = Motor._CarregarJournal(Id)
        if not R["ok"]:
            return R
        J = R["journal"]
        if J.get("estado") == "revertido":
            return {"ok": False, "motivo": "ja_revertido"}
        Restaurados = []
        for A in reversed(J.get("alvos") or []):
            if not A.get("backup"):
                continue
            Caminho = Manifesto.ResolverCaminho(A["arquivo"])
            Atual = Manifesto.HashArquivo(A["arquivo"])
            if A.get("hash_depois") and Atual.get("ok") and Atual["hash"][:12] != A["hash_depois"][:12]:
                return {"ok": False, "motivo": f"arquivo_mudou_desde_aplicacao:{A['arquivo']}",
                        "acao": "restauracao_abortada_para_nao_perder_trabalho"}
            Rst = Motor._RestaurarBackup(A["backup"], Caminho)
            if not Rst["ok"]:
                return {"ok": False, "motivo": Rst.get("motivo"), "restaurados": Restaurados}
            Restaurados.append({"arquivo": A["arquivo"], "de": A["backup"]})
        NovoJ = dict(J)
        NovoJ["estado"] = "revertido"
        NovoJ["revertido_em"] = Manifesto.Timestamp()
        try:
            with open(R["caminho"], "w", encoding="utf-8") as F:
                json.dump(NovoJ, F, ensure_ascii=False, indent=2)
        except Exception:
            pass
        return {"ok": True, "id": Id, "restaurados": Restaurados, "total": len(Restaurados)}

    @staticmethod
    def Diff(Id):
        R = Motor._CarregarJournal(Id)
        if not R["ok"]:
            return R
        J = R["journal"]
        Diffs = []
        for A in J.get("alvos") or []:
            Res = (A.get("resultado") or {})
            if "antes" in Res and "depois" in Res:
                Diffs.append({"arquivo": A["arquivo"], "linha": (Res.get("linhas_afetadas") or [None])[0],
                              "antes": Res["antes"].rstrip("\n"),
                              "depois": Res["depois"].rstrip("\n")})
            elif Res.get("tipo") == "substituir_texto":
                Diffs.append({"arquivo": A["arquivo"], "tipo": "substituir_texto",
                              "substituicoes": Res.get("substituicoes")})
            elif Res.get("tipo") == "remover_bloco":
                Diffs.append({"arquivo": A["arquivo"], "tipo": "remover_bloco",
                              "linhas_removidas": Res.get("linhas_removidas")})
        return {"ok": True, "id": Id, "diffs": Diffs, "total": len(Diffs)}

    @staticmethod
    def Journal(Id):
        return Motor._CarregarJournal(Id)

    @staticmethod
    def ListarAplicados():
        if not Motor._Garantir(Motor.JOURNAL):
            return {"ok": False, "motivo": "journal_indisponivel", "aplicados": []}
        Aplicados = []
        Erros = []
        for Arq in sorted(os.listdir(Motor.JOURNAL)):
            if not Arq.endswith(".json"):
                continue
            Caminho = os.path.join(Motor.JOURNAL, Arq)
            try:
                with open(Caminho, "r", encoding="utf-8") as F:
                    J = json.load(F)
            except Exception as E:
                Erros.append({"arquivo": Arq, "motivo": str(E)})
                continue
            if J.get("estado") == "aplicado":
                Aplicados.append({"id": J.get("id"), "timestamp": J.get("timestamp"),
                                  "alvos": len(J.get("alvos") or [])})
        return {"ok": True, "aplicados": Aplicados, "erros": Erros, "total": len(Aplicados)}


