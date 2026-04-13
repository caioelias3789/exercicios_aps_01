from __future__ import annotations


class Musico:
    def __init__(self, nome: str):
        self.nome = nome

    def exibir(self) -> dict:
        return {"Nome": self.nome}


class Musica:
    def __init__(self, titulo: str, duracao: str):
        self.titulo = titulo
        self.duracao = duracao

    def exibir(self) -> dict:
        return {
            "Título": self.titulo,
            "Duração": self.duracao
        }


class CD:
    def __init__(self, titulo: str, ano_lancamento: int, coletanea: bool, duplo: bool):
        self.titulo = titulo
        self.ano_lancamento = ano_lancamento
        self.coletanea = coletanea
        self.duplo = duplo
        self.musicos: list[Musico] = []
        self.musicas: list[Musica] = []

    def cadastrar(self) -> None:
        pass

    def exibir(self) -> dict:
        return {
            "Título": self.titulo,
            "Ano": self.ano_lancamento,
            "Coletânea": "Sim" if self.coletanea else "Não",
            "Duplo": "Sim" if self.duplo else "Não",
            "Músicos": ", ".join(m.nome for m in self.musicos) if self.musicos else "-",
            "Músicas": ", ".join(m.titulo for m in self.musicas) if self.musicas else "-"
        }

    def listar_musicos(self) -> list[str]:
        return [m.nome for m in self.musicos]

    def listar_musicas(self) -> list[str]:
        return [m.titulo for m in self.musicas]

    def adicionar_musico(self, musico: Musico) -> None:
        if all(m.nome.lower() != musico.nome.lower() for m in self.musicos):
            self.musicos.append(musico)

    def adicionar_musica(self, musica: Musica) -> None:
        if all(m.titulo.lower() != musica.titulo.lower() for m in self.musicas):
            self.musicas.append(musica)


class ColecaoCD:
    def __init__(self):
        self.cds: list[CD] = []

    def adicionar_cd(self, cd: CD) -> None:
        self.cds.append(cd)

    def listar_cds(self) -> list[dict]:
        return [cd.exibir() for cd in self.cds]

    def buscar_cds_por_musico(self, nome: str) -> list[CD]:
        resultados = []
        for cd in self.cds:
            for musico in cd.musicos:
                if nome.lower() in musico.nome.lower():
                    resultados.append(cd)
                    break
        return resultados

    def buscar_cds_por_musica(self, titulo: str) -> list[CD]:
        resultados = []
        for cd in self.cds:
            for musica in cd.musicas:
                if titulo.lower() in musica.titulo.lower():
                    resultados.append(cd)
                    break
        return resultados