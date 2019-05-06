import os
import numpy as np

if __name__ == '__main__':  # Otázka_1: víš, k čemu je tuta řádka?
    # užitečný na spojování cesty, protože každý operační systém to může mít jinak s lomítkama a podobně
    # knihovna os má hotové funkce na střihání strnigu s cestou na cesta a název souboru, procházení adresáře, a spoustu dalších
    # jde to samozřejmě řešit na úrovní stringu, ale tohle ušetří milion práce
    path_to_data = '/home/jedle/data/SL/data_prep/dict_solved'
    bvh_file = os.path.join(path_to_data, 'projevy_pocasi_02_solved_body.bvh')

    with open(bvh_file, 'r') as f:  # tuto je elegantní a čistý způsob četení souboru ('r' - read, 'w' - write (smaže soubor), 'a' - append (nesmaže soubor)
        content = f.readlines()  # promennou content naplní listem řádků

    print(type(content))  # tohle ti pomůže zjistit typ proměnné (protože se nedeklarují explicitně, tak občas nevíš jestli je to list, numpy array, float, integer a pod.)
    print(len(content))  # tohle je in-build knihovna a u numpy matic funguje pro mě nepředvidatelně
    print(np.shape(content))  # numpy shape umí vrátit i délku listu a doporučuji ;)

    content_short = content[:20]  # tady jenom ustříhnu kousek na začátku, aby se to dalo rozumně printit

    # for cykly umí python docela hezky kompaktně, ale nevím, jak moc je to přehledný pro začátečníka (pro mě je to furt matoucí, ale zdá se to pythonovitěji)
    # př1. tuto je taková klasika:
    for i in range(np.size(content_short, 0)):
        print(content_short[i])

    # př2. přes list jde iterovat i takhle, pokud nepotřebuješ sledovat číslo iterace:
    for item in content_short:
        print(item)

    # př2.5 přes list jde dělat i tuto, pokud potřebuješ sledovat číslo iterace:
    for i, item in enumerate(content_short):
        print(i, item)

    # př3. tuto je totálně pythonic, ale je to asi* jenom jednoduchou jednořádkovou operaci: (* jsem noob a vim prd, tak si netroufnu nic tvrdit na jistotu;) )
    # print([i if 'Frames' in con for i, con in enumerate(content)])

    # přípravím pro tebe data, můžeš se inspirovat.
    # expertní znalost BVH dat -> MOTION je první řádek po hyerarchii, proto hledám jeho index, abych uřízl ty motion data (ty čísla dole;) )
    index = ([x for x, con in enumerate(content) if 'MOTION' in con])  # hodně pythonický způsob jak dát if do for cyklu, zkus se nad tím zamyslet. Já to sám teprve adaptuju, ale stojí to za to.
    # pozn. vrací list (i jednoprvkový !)
    print('poslední řádek je tedy tuto: {}, a obsahovat by měl \'}}\' k ROOTU '.format(index[0]-1))  # to -1 je tam protože chci index tý složený závorky (kouni v texťáku do toho souboru, jak vypadá
    # , joa koukni na ty escapey pro spec. znaky
    print('vrací to složenou závorku?')
    print('ano' if '}' in content[index[0]-1] else 'ne')  # zase pythonický if-else. Pro jednoduchou věc je to dobrý, pro složitější bych to napsal asi normálně ukecaně, aby to bylo přehlednější

    # A nyní úloha: zkus to naparsovat a udělat nějakej výstup ála slovník. Je to furt trochu samoúčelné, ale myslím že dobrej trénink.
    # jenom vysvětlení: je tam vždycky JOINT jméno(u prvního ROOT) a jeho vlastnosti {OFFSET, [Channels], [JOINT POTOMEK, [JOINT Druhej potomek]]}

    # Zkus a uvidíš, kde se zasekneš. Mysli na to, že pochopení a elegance (efektivita a absence překombinovaných funkcí) kódu je cílem ;)
    data_pro_tebe = content[:index[0]-1]
