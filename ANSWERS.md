# Semaine 3

### Question 1 : Comment avez-vous conçu la lecture du fichier ? Comment l’avez-vous structurée de sorte à pouvoir la tester de manière efficace ?

La lecture du fichier se fait à travers la méthode create_map() de la classe GameView. Cette méthode est appelée par setup(), d'où elle tire également l'emplacement du fichier qu'elle doit lire. 
Elle vérifie que le fichier ait un format valable au fil et à mesure de la lecture. Si le fichier n'a pas la bonne structure, la méthode envoie une exception. 
Ainsi, la méthode est testée en créant une instance de GameView avec comme argument différents fichiers tests, certains valables et d'autre pas. Les fichier non-valables sont testés en vérifiant que la méthode renvoie bien la bonne exception, et stockés dans le dossier "maps/bad_maps".
main() s'occupe ensuite des exceptions lancées par create_map(), en imprimant l'exception dans la console.


### Question 2 : Comment avez-vous adapté vos tests existants au fait que la carte ne soit plus la même qu’au départ ? Est-ce que vos tests résisteront à d’autres changements dans le futur ? Si oui, pourquoi ? Si non, que pensez-vous faire plus tard ?

Nous avons recrée la map de départ dans un fichier nommé "default_map.txt". Le chemin de ce fichier est passé par défaut à GameView, si aucun autre argument n'est donné pour le chemin de la map. Les tests existants n'ont alors pas dû être modifiés. On aurait aussi pu simplement passer le chemin de cette map à tous les tests déjà écrits. Il se peut que nous fassions cela plus tard, s'il pour une raison quelconque nous devons changer la map proposée par defaut. Nous ne voyons pas de raison pour laquelle les tests ne résisteraient pas à d'autres changements (raisonnables) dans le futur, surtout si la méthode de passer la map à GameView ne change pas. Il sera à priori toujours possible de choisir quel map utiliser pour chaque test individuellement.

### Question 3 Le code qui gère la lave ressemble-t-il plus à celui de l’herbe, des pièces, ou des blobs ? 
Le code qui gere la lave est proche de celui qui gere la lave car il fait la meme chose, il tue la joueuse en recommencent le niveau.
Sinon la  lave resmenle un peu au pieces car c'est un objet amovible qui a une inteaction avec la joueuse.

### Question 4 Comment détectez-vous les conditions dans lesquelles les blobs doivent changer de direction ?
-pour les colision avec les mur je test pour chaques blobs si il est a l'interieur d'un mur si oui il change de direction sinon il continue a avancer
-pour le bord des plateformes je fais un peut comme la fonction is on ground est definit: j'avance le blob de sa longeur dans le sens de son deplacement et ensuite je l'abaisse de quelques unite temporairement et je check si le blob est en colision avec un mur si le blob est en colision avec un mur alors sa prochaine position est entierement sur le sol et il continue d'avencer  sinon il va tomber et donc il fait demi tour

# Semaine 4

### Question 1 (Paul) :Quelles formules utilisez-vous exactement pour l’épée ? Comment passez-vous des coordonnées écran aux coordonnées monde ?
j'utillise cette formule pour calculer la difference entre la position de la souris et celle de la joueuse
    delta_x=mouse_x+self.__camera.bottom_left.x-self.__player.center_x
    delta_y=mouse_y+self.__camera.bottom_left.y-self.__player.center_y-5
ensuite j'utilise l'arctangente (atan2(delta_x,delta_y)) pour calculer l'angle

les coordonees de l'ecran commencent en bas a gauche donc j'utilise les coordonees point en bas a gauche de la camera auquelle j'ajoute les coordone de la souris pour passer au coordonée monde


### Question 2 (Paul) :Comment testez-vous l’épée ? Comment testez-vous que son orientation est importante pour déterminer si elle touche un monstre ?

je test juste en faisant une map ou la joueuse aparait a côté d'un blob et on verifie si le blob moeur quand on utilise l'épée 
dans la direction du blob


### Question 4 (Paul):Comment transférez-vous le score de la joueuse d’un niveau à l’autre ?

on transfere le score en ne reinitialisant pas la joueuse d'un niveau a l'autre. 


### Question 3 (Paul) :Où le remettez-vous à zéro ? Avez-vous du code dupliqué entre les cas où la joueuse perd parce qu’elle a touché un ou monstre ou de la lave ?
le score est initialiser en meme temps que la joueuse du coup il est remis a zero lors de l'inintialisation lors de la mort de la joueuse .



### Question 5 (Gaëlle) : Comment modélisez-vous la “next-map” ? Où la stockez-vous, et comment la traitez-vous quand la joueuse atteint le point E ?

La next map est le chemin du prochain niveau, qui est stocké comme string dans un attribut de la class GameView. Cet attribut est mis à jour à chauque fois qu'une nouvelle map est crée par la méthode create_map(). Quand la joueuse atteint le point E, la méthode load_next_map() est appelée. Cette méthode s'assure que le nom de la prochaine map est bien stockée, puis remplace la map actuelle par la prochaine map dans l'attribut current_map_name, avant d'appeler la méthode setup qui crée le prochain niveau. 

### Question 6 (Gaëlle) : Que se passe-t-il si la joueuse atteint le E mais la carte n’a pas de next-map ?

Si la joueuse atteint le point E mais que la carte n'a pas de next-map, nous considérons que le joueur a gagné le jeu. Alors, nous affichons un message de victoire, dont la seule façon de quitter et de fermer la fenêtre du jeu.

# Semaine 5 (Arc et chauves-souris)

### Question 1 (Paul):Quelles formules utilisez-vous exactement pour l’arc et les flèches ?

l'arc utilise plus ou moins la meme formule que pour l'épée (c'est une instance de Weapon)
les fleches elles font une parabole donc on une compiosantes acceleration verticale et on un angle qui est calculer via 
le rartio vitesse x et vitesse y et l'atan2

### Question 2 (Gaëlle) : Quelles formules utilisez-vous exactement pour le déplacement des chauves-souris (champ d’action, changements de direction, etc.) ?

Le champ d’action de chaque chauve-souris est un disque de rayon constant, centré autour de sa position d’origine.
Toutes les BAT_FRAMES frames, ou lorsqu’elle ne peut plus avancer dans sa direction actuelle sans sortir de ce disque, la chauve-souris choisit un angle aléatoire selon une distribution gaussienne centrée en 0 avec un écart-type de 20 degrés.
Elle ajoute cet angle à sa direction actuelle (mesurée par rapport au centre du disque).
Si elle peut se déplacer dans cette nouvelle direction tout en restant dans son champ d’action, elle adopte cette nouvelle direction. Sinon, elle tire un autre angle jusqu’à ce qu’un déplacement valide soit trouvé.

### Question 3 (Paul) : Comment avez-vous structuré votre programme pour que les flèches puissent poursuivre leur vol ?:Comment avez-vous structuré votre programme pour que les flèches puissent poursuivre leur vol ?

les fleches sont stoquer dans une liste et chaques frames on vas chercher si les fleches restent dans les conditions adequates pour poursuivre leur vol sinon on les suprimes de la liste

### Question 4 (Paul et Gaëlle) : Comment gérez-vous le fait que vous avez maintenant deux types de monstres, et deux types d’armes ? Comment faites-vous pour ne pas dupliquer du code entre ceux-ci ?

Nous avons crée deux classes abstraites Monster et Weapon, qui sont respectivement les classes parent de Bat et Blob (notamment), et de Bow et Sword. C'est classes implémentent les méthodes communes à leurs sous-classes, et définissent des méthodes abstraites que toutes leurs sous classes doivent implémenter, afin de pouvoir utilser le polymorphisme dans gameview, notamment en itérant par dessus des listes de monstres sans devoir vérifier leur type. Les sous_classes n'ont pas d'autre méthodes publiques et celles définies dans leur superclasse.

# Semaine 8 (Plateformes et interrupteurs)

### Question 1 (Gaëlle) : Quel algorithme utilisez-vous pour identifier tous les blocs d’une plateformes, et leurs limites de déplacement ?

Nous utilisons un algorithme récursif qui démarre à partir d’un bloc de plateforme et explore tous les blocs adjacents non diagonaux.
Si un bloc n’a pas encore été visité et qu’il s’agit d’un bloc de plateforme, il est ajouté à la plateforme, et l’algorithme poursuit l’exploration de ses voisins.
Si le bloc n’est pas un bloc de plateforme, l’exploration ne continue pas depuis ce bloc.
Toutefois, si le bloc est une flèche, l’algorithme vérifie si son orientation est compatible avec sa position par rapport à la plateforme (par exemple, une flèche vers le haut ne doit pas se trouver à gauche d’un bloc de plateforme).
Si la flèche est bien positionnée, l’algorithme continue son exploration uniquement dans la direction indiquée, tant qu’il ne rencontre que des flèches pointant dans cette même direction. Ces flèches sont comptées afin de déterminer les limites de déplacement de la plateforme.

### Question 2 (Gaëlle) : Sur quelle structure travaille cet algorithme ? Quels sont les avantages et inconvénients de votre choix ?
L'algorithme se sert d'un ensemble de tuples de nombres entiers pour les positions déjà visitées. Nous avons choisi cette structure car les deux seules opérations que nous voulons faire dessus sont l'ajout d'un nouvel élément et la vérification de l'appartenance d'un élément à l'ensemble, et ces deux opérations sont très efficaces avec un ensemble.
Pour créer les platformes, nous travaillons sur une classe que nous avons défini, dans laquelle nous stockons les positions initiales des blocs de la plateforme également dans un ensemble de tuples d'entiers. Les deux seules opérations que nous faisons dessus sont à nouveau la vérification d'appartenance et l'ajout d'un élément.

### Question 3 (Paul) : Quelle bibliothèque utilisez-vous pour lire les instructions des interrupteurs ? Dites en une ou deux phrases pourquoi vous avez choisi celle-là.

### Question 4 (Paul) : Comment votre design général évolue-t-il pour tenir compte des interrupteurs et des portails ?
