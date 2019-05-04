import numpy as np
import matplotlib.pyplot as plt


def funkce(x):
    return np.sin(x)

if __name__ == '__main__':
    x = 5
    print('sinus {} je {:.2f} na dvě desetiný místa.'.format(x, funkce(x)))
    print('---------------')
    vektor = np.array([2, 3, 4])
    print('vektor: ' + str(vektor))
    print('---------------')
    print('matice: \n' + str(np.array([[2, 3], [5, 6]])))
    print('---------------')
    matice = np.array(range(100))
    print(matice)
    print('---------------')
    matice2 = matice + 2 * 5
    print(matice2)
    print('---------------')
    print(matice2[5])
    print('---------------')
    print(matice2[:5])
    print('---------------')
    print(matice2[5:])
    print('---------------')
    print(matice2[5:7])
    print('---------------')
    vysledek = funkce(matice*0.1)
    vysledek2 = np.cos(matice*0.1)
    print()

    plt.plot(vysledek)
    plt.plot(vysledek2)
    plt.show()

    string_na_rozloucenou = ''
    string_na_rozloucenou += 'Informace tady v tom kódu ti nejspíš nestačí k řešení následující úlohy. \n'
    string_na_rozloucenou += 'Můj kod je fakt takovej hello world, abys měl kde začít, pokud nevíš.\núlohou chci zjistit jak jsi na tom, takže chci kody!\n'
    string_na_rozloucenou += 'ZADANI:\nudělat matici obsahující data, kde plot matice bude mít výstup podobný tutomu (Projec.png)\n'
    string_na_rozloucenou += 'tím plotem myslím, aby prikaz byl přesně tuto: plt.plot(matice)\n'

    for i in range(20):
        string_na_rozloucenou += 'pápá '

    print(string_na_rozloucenou)
