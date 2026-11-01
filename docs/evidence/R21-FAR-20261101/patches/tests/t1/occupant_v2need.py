from pipd_ls_sp.abi import Need
NEED = Need("cap.attest", 2, ("identity",))
class Impl:
    def identity(self):
        return "cap-attest-v2"
def build():
    return Impl()
