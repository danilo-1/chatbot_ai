import subprocess, os, tempfile, re

class ProcessService:
    def extrair_dependencias_dos_imports(self, codigo: str) -> list[str]:
        pattern = r"^(?:import|from)\s+([\w\.]+)"
        modulos = re.findall(pattern, codigo, re.MULTILINE)
        modulos_padroes = ["os", "sys", "re", "json", "time", "datetime", "math", "random", "platform", "subprocess", "tempfile"]
        return list(set(m for m in modulos if m not in modulos_padroes))

    def executar_codigo_docker(self, codigo, pacotes: list[str] = None):
        dependencias_dos_imports = self.extrair_dependencias_dos_imports(codigo)
        pacotes = pacotes or []
        all_deps = list(set(dependencias_dos_imports + pacotes))

        with tempfile.NamedTemporaryFile("w", suffix=".py", delete=False, encoding="utf-8") as f:
            arquivo_temp = f.name
            f.write(codigo)

        caminho_absoluto = os.path.abspath(arquivo_temp)

        install_cmd = ""
        if all_deps:
            pacotes_str = ' '.join(all_deps)
            install_cmd = f"pip install {pacotes_str} && "

        comando = [
            "docker", "run", "--rm",
            "-v", f"{caminho_absoluto}:/app/codigo.py",
            "python:3.11",
            "bash", "-c",
            f"{install_cmd} python /app/codigo.py"
        ]

        try:
            resultado = subprocess.run(
                comando, capture_output=True, text=True, encoding="utf-8", timeout=120
            )

            if resultado.returncode == 0:
                saida = resultado.stdout.strip()
            else:
                if "KeyboardInterrupt" in resultado.stderr:
                    saida = "Execução interrompida pelo usuário."
                elif resultado.returncode == 130:
                    saida = "Execução interrompida pelo usuário."
                else:
                    saida = f"Erro na execução:\n{resultado.stderr.strip()}"

        except subprocess.TimeoutExpired:
            saida = "Erro: Código excedeu o limite de tempo!"
        except KeyboardInterrupt:
            saida = "Execução interrompida pelo usuário."
        finally:
            if os.path.exists(arquivo_temp):
                os.remove(arquivo_temp)
            return saida