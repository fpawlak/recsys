1. Opis danych i zagadnienia
2. Użyte metody
3. Opis implementacji
4. Testy
5. Wyniki
6. Podsumowanie, perspektywy rozwoju


#1. Opis danych i zagadnienia

Celem projektu było stworzenie systemu rekomendującego dla filmów. Posłużyliśmy się przy tym danymi MovieLens dostarczonymi przez GroupLens Research. Do wyboru były 3 zestawy danych o wielkości 100 tysięcy, 1 miliona, 10 milionów rekordów. Wybraliśmy pierwszy zestaw, który zawiera oceny dodane przez 1000 użytkowników na 1700 filmach. Wybór podyktowany był zbyt dużymi kosztami obliczeniowymi przy większych zestawach danych. Każdy użytkownik musiał dodać co najmniej 20 ocen. Należy zwrócić uwagę, że macierz uzyskana z dostarczonych ocen jest rzadka, ponieważ uzupełnionych jest mniej niż 6% elementów. Oceny możlwie do wystawienia przez użytkowników to 1, 2, 3, 4, 5.


#2. Użyte metody

Przy ustalaniu wyboru metod sugerowaliśmy się tym, by można je było zaimplementować i przetestować w rozsądnym czasie, oraz żeby otrzymane wyniki były jak najlepsze. W tym celu pod uwagę wzięliśmy metody poznane na wykładzie oraz zapoznaliśmy się z wieloma dokumentami nt. Netflix Prize, aby dowiedzieć się, które metody okazały się najbardziej skuteczne w owym konkursie. Chcieliśmy również wybrać co najmniej 2 metody, tak by można było je porównać oraz zastosować razem.

Z wykładu została wybrana metoda Slope One, która jest rozszerzeniem Collaborative Filtering. Główna idea polega na zastosowaniu regresji w uproszczonej formie. Wg autorów to właśnie dzięki jej prostocie (w kontekście wyboru bazy dla regresji) uzyskiwane są dobre wyniki.

Drugim wyborem była metoda SVD, która przez wiele osób została oceniona jako jedna z lepszych metod dla systemów rekomendujących. Jest ona podobna do PCA. Główna idea polega na usunięciu szumów z danych poprzez przejście do niższego wymiaru. Na początku wykonujemy dekompozycję macierzy na 3 specyficzne macierze, z których środkowa jest diagonalna, a lewa i prawa są ortonormalnymi macierzami przejścia/powrotu do/z nowej przestrzeni (takiego samego wymiaru jak pierwotnie). W nowej przestrzeni w sposób trywialny możemy sprawdzić, które wymiary odpowiadają za najmniejszą wariancję i je usunąć poprzez wyzerowanie odpowiadającym im wartości własnych (są to najmniejsze wartości własne).


#3. Opis implementacji

##3.1. Slope One

Metoda Slope One została zaimplementowana w klasie SlopeOne. Obiekt tej klasy przechowuje wyniki przetwarzania wstępnego niezbędne do dalszych obliczeń (m.in. średnie różnice pomiędzy wszystkimi parami filmów).

Niech n oznacza liczbę filmów, m - liczbę użytkowników, zaś N - liczbę ocen w bazie.

Policzenie wszystkich różnic wymaga czasu O(my^2 + n^2), gdzie y jest oszacowaniem górnym na liczbę filmów, które ocenił pojedynczy użytkownik. W implementacji algorytmu istotne jest, żeby licząc różnice iterować tylko po filmach, które użytkownik ocenił, nie zaś po wszystkich filmach w bazie (co spowoduje wzrost złożoności do O(mn^2)). Dlatego funkcja computeDiffs operuje na rzadkiej reprezentacji danych.

Predykcja pojedynczej oceny wymaga czasu O(x), gdzie x to liczba filmów, które ocenił użytkownik. Predykcja ocen wszystkich nieocenionych filmów dla pojedynczego użytkownika wymaga czasu O((n - x) * x).

##3.2. SVD

Ze względu na szerokie zastosowanie tej metody, większość języków ma ją zaimplementowaną w swoich bibliotekach. Tak jest również w przypadku Pythona, dlatego implementacja sprowadza się do dostosowania tej metody do naszych danych oraz kalibracji.

Aby zastosować ową metodę należy mieć macierz wypełnioną w 100%, a my mamy tylko niecałe 6%. Proponowane rozwiązanie to policzenie średniej dla każdego filmu i wstawienie odpowiednich liczb w brakujące pola. W 32 przypadkach okazuje się, że film nie ma żadnej oceny. Proponowane w różnych dokumentach rozwiązanie to wstawienie zera. Rozważyliśmy również wstawienie średniej dla wszystkich filmów. Sprawdziliśmy oba rozwiązania na małej próbce danych i zgodnie z intuicjami, drugie rozwiązanie okazało się lepsze, dlatego je zastosowaliśmy.

Ostatnią kwestią zostaje ustalenie tego jak dużo szumu chcemy usunąć, tj. ile wartości własnych zostanie wyzerowanych. W naszym podejściu chcemy zostawić taką liczbę wartości własnych, których suma odpowiada konkretnej części sumy wszystkich wartości własnych. Sposób w jaki wyznaczamy ten poziom jest opisany w kolejnej sekcji. W programie poziom ten jest argumentem do funkcji zwracającej macierz po SVD i jest oznaczony jako 'level'.

Zastosowaliśmy również połączenie obu metod. W przypadku SVD puste miejsca w macierzy uzupełniliśmy średnimi dla każdego filmu, co było dużym uproszczeniem. Zamiast tego najpierw stosujemy metodę Slope One, która uzupełnia wszystkie pola w macierzy i dopiero wtedy zostaje ona przetworzona przez SVD.


#4. Testy

W celu sprawdzenia jakości zastosowanych metod wykonaliśmy wiele testów. Główna idea naszych testów to iteracja po wszystkich danych z paczki MovieLens i usuwanie po kolei pojedynczych ocen. Za każdym razem uzyskane w ten sposób dane traktujemy jakby były to zupełne nowe dane i sprawdzamy predykcję brakującej oceny. Sprawdzamy czy nie rożni się ona o więcej niż o 0,5 od prawidłowej wartości (czyli zaokrąglamy wynik uzyskany przez algorytm i sprawdzamy czy jest taki sam jak oryginalny). Jeżeli tak, to predykcja zostaje uznana za prawidłową. Wydaje się, że jest to znacznie lepsza metoda, niż podział danych na uczące i testowe w stosunku 80/20 (który zaproponowali autorzy danych).

Minusem tego rozwiązania jest to, że trzeba 100 tys. razy uruchomić algorytm. W przypadku Slope One nie trzeba wszystkiego liczyć od nowa, dlatego w czasie mniejszym niż 30 minut jesteśmy w stanie sprawdzić cały zbiór danych. W przypadku SVD za każdym razem trzeba dokonać dekompozycji całej macierzy i jest to proces zbyt czasochłonny. Istnieją algorytmy pozwalające dodać nowy wiersz lub kolumnę bez przeliczania całej macierzy, lecz przydatne jest to przy np. wprowadzaniu nowych użytkowników do bazy, a w naszym przypadku chcemy usunąć jeden element, a nie coś dodać. Proponujemy zatem dwa rozwiązania:

a) Losujemy np. 10% danych (tutaj: 10 tys.) i tylko dla tych danych sprawdzamy predykcje.

b) Dane dzielimy losowo na grupy k-elementowe (np. K = 100) i zamiast usuwać w jednym momencie tylko jeden element, to usuwamy k elementów. Dzięki temu cały algorytm musimy uruchomić 100000/k razy mniej, co pozwala nam sprawdzić wszystkie dane w rozsądnym czasie.

Podsumowując, testy jakie wykonujemy to:

i. Slope One z wyciąganiem pojedynczym na całych danych (100%)

ii. SVD z wyciąganiem pojedynczym na części danych (10%)

iii. SVD z wyciąganiem pojedynczym w grupach po 100 elementów na całych danych (100%)

iv. Połączenie Slope One z SVD z wyciąganiem pojednczym na części danych (10%)

Oprócz tego potrzebujemy skalibrować SVD, tj. ustalić poziom, od którego zerujemy wartości własne. Skorzystaliśmy z testowania opisanego jako wyciąganie pojedyncze w grupach. Dla tej same próby danych (1%) sprawdziliśmy wyniki dla różnych poziomów na przedziale od 0,3 do 0,9 z krokiem co 0,05. Ograniczlismy w ten sposób przedział do [0,35 ; 0.50]. Wykonaliśmy test ponownie dla nowego przedziału z krokiem co 0,03. Ostatecznie najlepszym poziomem okazało się 0,47. Teoretycznie można było również próbować badań z mniejszymi krokami oraz na większej próbie danych, ale różnice nie były aż tak duże.

Dane, na których wykonywaliśmy testy (MovieLens 100k), znajdują się w pliku data/u.data. Ponadto zapisaliśmy niektóre pośrednie rezultaty obliczeń dla Slope One (z powodu ich kosztowności):

https://www.dropbox.com/s/rowqtm9esepbjmv/macierz-wypelniona.txt

https://www.dropbox.com/s/o9n1vyaao5mgxmd/num.txt

https://www.dropbox.com/s/s4kt5biyonmq70u/den.txt

Przykład użycia znajduje się w pliku źródłowym src/s1.py.

#5. Wyniki

Wyniki testów:

i. 41,6% (Slope One)

ii. 40,5% (SVD)

iii. 40,6% (SVD grupami)

iv. 43,0% (Slope One + SVD)




Zostały również przeprowadzone analogiczne testy, ale sprawdzające czy przewidywana przez algorytm wartość nie różni się o więcej niż 1 od oryginalnej. Oto wyniki:

i. 89,7% (Slope One)

ii. 89,3% (SVD)

iii. -

iv. 90,2% (Slope One + SVD)




W katalogu /src/results/ znajdują się również wyniki pośrednie dla testów ii-iv (zapisywane po sprawdzeniu np. każdej setki próbek).

#6. Podsumowanie

Najlepsze rezultaty dało wspólne zastosowanie obu algorytmów. Mimo wielu głosów za SVD, okazało się, że w bezpośredniej konfrontacji to Slope One był nieco lepszy. Być może wynika to ze specyfiki danych.

W realnym zastosowaniu algorytmu SVD (lub obu naraz) warto zainteresować się metodą zaproponowaną przez Matthew Branda, która pozwala dodać jeden wiersz lub kolumnę do danych bez ponownej dekompozycji macierzy danych.

Interesującym rozwinięciem SVD jest też zastosowanie algorytmów grupujących (np. k-means) do znalezienia osób o podobnych zainteresowaniach.

Wartym sprawdzenia byłoby również użycie Bi-Polar Slope One.

Wciąż nie do końca (w naszych rozważaniach) rozwiązana zostaje kwestia osób, które mają upodobania w kilku zupełnie różnych gatunkach i przez to nie są “podobne” do osób, które interesują się tylko jednym z tych gatunków.
