# Semaine 3

### Question 1 : Comment avez-vous conçu la lecture du fichier ? Comment l’avez-vous structurée de sorte à pouvoir la tester de manière efficace ?

La lecture du fichier se fait à travers les méthodes __create_map() et __parse_config() de la classe `Map`. Ces méthodes sont appellées par l'__init__ de `Map`. Une instance de `Map` est crée dans setup() de `GameView`, d'où elle tire également l'emplacement du fichier qu'elle doit lire et les listes de sprites qu'elle soit remplir. 
`Map` vérifie que le fichier ait un format valable au fil et à mesure de la lecture. Si le fichier n'a pas la bonne structure, les méthodes envoient une exception. 
Ainsi, la méthode est testée en créant plusieurs instances de `GameView`, prennant en argument différents fichiers tests, certains valables et d'autre pas. Les fichier non-valables sont testés en vérifiant que la méthode renvoie bien la bonne exception, et stockés dans le dossier "maps/bad_maps".
`GameView` s'occupe ensuite des exceptions lancées par `Map`, en imprimant le message d'erreur dans une View de `GameView`. 


### Question 2 : Comment avez-vous adapté vos tests existants au fait que la carte ne soit plus la même qu’au départ ? Est-ce que vos tests résisteront à d’autres changements dans le futur ? Si oui, pourquoi ? Si non, que pensez-vous faire plus tard ?

Nous avons recrée la map de départ dans un fichier de chemin "maps/testing_maps/default_map.txt". Pour ne pas modifier les tests existant, nous avons simplement passé ce fichier en argument de `GameView` pour les tests qui étaient déjà écrits, afin que leur comportement ne change pas. Pour les écrits après ce changement, nous avons choisis sur quel fichier ils devaient se dérouler, alors la map qui est choisie par l'utilisateur n'a pas d'impact sur les tests. Les fichiers servant aux tests ne doivent surtout pas être modifiés, c'est pourquoi nous les avons tous regroupés dans le dossier "maps/testing_maps". Nous ne voyons pas de raison pour laquelle les tests ne résisteraient pas à d'autres changements (raisonnables) dans le futur, surtout si la méthode de passer la map à GameView ne change pas. Il sera à priori toujours possible de choisir quel map utiliser pour chaque test individuellement. Nous avons également ajouté la possibilité de choisir le fichier directement depuis le terminal, mais comme dit précédemment, le choix de fichier fait par l'utilisateur n'a pas d'impact sur les tests.

### Question 3 Le code qui gère la lave ressemble-t-il plus à celui de l’herbe, des pièces, ou des blobs ?

Il ressemblait initialement à celui de l'herbe, étant un Sprite immobile, à la différence près qu'une collision avec la lave tuait le joueur. Maintenant, après avoir ajouté les platformes, la lave soit parfois être bougée par une méthode que nous avons écrit nous-mêmes, au contraire du mouvement de l'herbe qui est géré par Arcade. Nous pouvons alors dire que le code du mouvement a quelques similaritées avec celui faisant bouger les blobs. Finalement, l'idée ressemble un peu aux pièces, car la joueur peut intéragir avec, au contraire des murs qui ne font que le bloquer.

### Question 4 Comment détectez-vous les conditions dans lesquelles les blobs doivent changer de direction ?

Pour les collisions avec des murs qui lui bloquerait le chemin, nous testons pour chaque blob s'il est à l'intérieur d'un mur. Si c'est le cas, il doit changer de direction en inversant sa vitesse. Sinon, il continue son chemin.

Pour voir si le blob a atteint le bord de sa platforme (dans son sens immobile, ici), on fait un réflexion similaire à celle faite dans la fonction can_jump du PhysicsEnginePlatformer d'Arcade. 
Nous faisons avancer le blob d'un tick dans son sens de déplacement, puis l'abaissons de quelque pixels. Nous vérifions si le blob est en collision avec un mur. Si c'est le cas, on le remet à sa place initiale sans changer sa direction de mouvement. Sinon, nous savons que le blob tomberait la prochaine fois qu'il avance, alors nous le remettons à sa place et inversons la direction de son mouvement.

# Semaine 4

### Question 1 : Quelles formules utilisez-vous exactement pour l’épée ? Comment passez-vous des coordonnées écran aux coordonnées monde ?
Nous utilisons la formule suivante pour calculer la difference entre la position de la souris et celle de la joueuse :

    delta_x = world_mouse_x - player_position.x
    delta_y = world_mouse_y - player_position.y - constants.WEAPON_OFFSET_Y

Puis, nous utilisons l'arctangente atan2(delta_x,delta_y) pour calculer l'angle que doit avoir l'épée

    self.angle = atan2_deg(delta_x, delta_y) - self.__texture_angle

Les coordonées de l'écran commencant en bas à gauche, nous utilisons les coordonées du coin gauche inférieur de la caméra,auquel nous ajoutons les coordonnées de la souris, pour passer aux coordonées monde :

    world_mouse_x = mouse_position.x + camera_bottom_left.x
    world_mouse_y = mouse_position.y + camera_bottom_left.y


### Question 2 : Comment testez-vous l’épée ? Comment testez-vous que son orientation est importante pour déterminer si elle touche un monstre ?

Nous testons en faisant une map où la joueuse apparait à côté d'un blob, et nous vérifions si le blob meurs au coup d'épée.
Puis nous testons en changant la direction de l'épée, et en s'assurant que cette fois-ci, le blob ne meurs pas.
Dans `GameView`, nous avons du bloquer la fonctionnalité que l'épée suive la souris, pour les tests, afin que la position de la souris n'aie pas d'impact sur la réussite des tests.

### Question 4 : Comment transférez-vous le score de la joueuse d’un niveau à l’autre ?

Une nouvelle instance de Player() est crée à chaque fois qu'on recommence à partir du premier niveau, mais pas quand on passe d'un niveau à l'autre. Comme le nombre de pièces que la joueuse a ramassé est stocké dans player, cela permet de garder le score d'un niveau à l'autre. Lorsqu'un nouveau niveau est chargé, sans créer de nouveau joueur, seules les coordonnées du joueur sont mises à jour. Ainsi, le joueur garde aussi son choix d'arme d'un niveau à l'autre.

### Question 3 : Où le remettez-vous à zéro ? Avez-vous du code dupliqué entre les cas où la joueuse perd parce qu’elle a touché un ou monstre ou de la lave ?

Nous le mettons à zéro lors de la création d'une nouvelle instance de joueur, directement de son __init__. Dans GameView, une nouvelle instance de Player() est crée dans la fonction __setup_from_initial(), qui est appelée dès qu'il faut recommencer depuis le premier niveau, peu importe la raison. Ainsi, il n'y a pas de duplication de code.

### Question 5 : Comment modélisez-vous la “next-map” ? Où la stockez-vous, et comment la traitez-vous quand la joueuse atteint le point E ?

La next map est le chemin du prochain niveau, qui est stocké comme string dans un attribut de la classe `GameView`. Cet attribut est mis à jour à chaque fois qu'une nouvelle map est chargée par la classe `Map`. Quand la joueuse atteint le point E, la méthode load_next_map() est appelée. Cette méthode s'assure que le nom de la prochaine map est bien stockée, puis remplace la map actuelle par la prochaine map dans l'attribut current_map_name, avant d'appeler la méthode setup qui crée le prochain niveau.

### Question 6 : Que se passe-t-il si la joueuse atteint le E mais la carte n’a pas de next-map ?

Si la joueuse atteint le point E mais que la carte n'a pas de next-map, nous considérons qu'elle a gagné le jeu. Alors, nous affichons un message de victoire, dont la seule façon de quitter est de fermer la fenêtre du jeu. C'est la même idée que si nous affichions un message d'erreur.

# Semaine 5 (Arc et chauves-souris)

### Question 1 :Quelles formules utilisez-vous exactement pour l’arc et les flèches ?

L'arc utilise les mêmes formules que l'épée, car ce sont deux sous-classes de `Weapon`, qui est la classe qui fait les calculs de position. Ici, nous faisons preuve de polymorphisme.
Les flèches, quant à elles, font des paraboles. Alors, elles ont une composante d'accélération verticale, mais pas d'accélération horizontale. Les vitesses initiales sont définies comme telles :

        self.change_x = constants.ARROW_SPEED*sin_deg(self.angle)
        self.change_y = constants.ARROW_SPEED*cos_deg(self.angle)

Puis mises à jour à chaque frame avec ces formules :
        
        self.change_y -= constants.ARROW_GRAVITY
        self.center_x += self.change_x
        self.center_y += self.change_y
        self.angle = atan2_deg(self.change_x, self.change_y) - 45

### Question 2 : Quelles formules utilisez-vous exactement pour le déplacement des chauves-souris (champ d’action, changements de direction, etc.) ?

Le champ d’action de chaque chauve-souris est un disque de rayon constant, centré autour de sa position d’origine.
Toutes les BAT_FRAMES frames, ou lorsqu’elle ne peut plus avancer dans sa direction actuelle sans sortir de ce disque, la chauve-souris choisit un angle aléatoire selon une distribution gaussienne centrée en 0 avec un écart-type de 20 degrés.
Elle ajoute cet angle à sa direction actuelle (mesurée par rapport au centre du disque).
Si elle peut se déplacer dans cette nouvelle direction tout en restant dans son champ d’action, elle adopte cette nouvelle direction. Sinon, elle tire un autre angle jusqu’à ce qu’un déplacement valable soit trouvé.

### Question 3 : Comment avez-vous structuré votre programme pour que les flèches puissent poursuivre leur vol ?

Les flèches sont stockées dans une liste de flèches. À chaque frame, soit on fait avancer les flèches comme décrit plus haut, soit on les supprime, si elles sont en collison avec un sprite. Chaque flèche est indépendante des autres, et indépendante de l'arc, du moment qu'elle a été tirée. Il n'y a alors pas de raison quelles ne puissent pas continuer leur vol.

### Question 4 : Comment gérez-vous le fait que vous avez maintenant deux types de monstres, et deux types d’armes ? Comment faites-vous pour ne pas dupliquer du code entre ceux-ci ?

Nous avons crée deux classes abstraites `Monster` et `Weapon`, qui sont respectivement les classes parent de `Bat` et `Blob` (notamment), et de `Bow` et `Sword`. Ces classes implémentent les méthodes communes à leurs sous-classes, et définissent des méthodes abstraites que toutes leurs sous-classes doivent implémenter, afin de pouvoir utilser le polymorphisme dans `GameView`, notamment en itérant par dessus des listes de monstres sans devoir vérifier leur type. Les sous-classes n'ont pas d'autre méthodes publiques et celles définies dans leur superclasse. Il n'y a alors pas de duplication de code entre les classes.

# Semaine 8 (Plateformes et interrupteurs)

### Question 1 : Quel algorithme utilisez-vous pour identifier tous les blocs d’une plateformes, et leurs limites de déplacement ?

Nous utilisons un algorithme récursif qui démarre à partir d’un bloc de plateforme et explore tous les blocs adjacents non diagonaux.
Si un bloc n’a pas encore été visité et qu’il s’agit d’un bloc de type autorisé à être dans une plateforme, il est ajouté à la plateforme, et l’algorithme poursuit l’exploration de ses voisins.
Si le bloc n’est pas un bloc de type autorisé à être dans une plateforme, l’exploration ne continue pas depuis ce bloc.
Toutefois, si le bloc est une flèche, l’algorithme vérifie si son orientation est compatible avec sa position par rapport à la plateforme (par exemple, une flèche vers le haut ne doit pas se trouver à gauche d’un bloc de plateforme).
Si la flèche est bien positionnée, l’algorithme continue son exploration uniquement dans la direction indiquée, tant qu’il ne rencontre que des flèches pointant dans cette même direction. Ces flèches sont comptées afin de déterminer les limites de déplacement de la plateforme.

### Question 2 : Sur quelle structure travaille cet algorithme ? Quels sont les avantages et inconvénients de votre choix ?

L'algorithme se sert d'un ensemble de tuples de nombres entiers pour les positions déjà visitées. Nous avons choisi cette structure car les deux seules opérations que nous voulons faire dessus sont l'ajout d'un nouvel élément et la vérification de l'appartenance d'un élément à l'ensemble, et ces deux opérations sont très efficaces avec un ensemble.
Pour créer les platformes, nous travaillons sur une classe que nous avons défini, dans laquelle nous stockons les positions initiales des blocs de la plateforme également dans un ensemble de tuples d'entiers. Les deux seules opérations que nous faisons dessus sont à nouveau la vérification d'appartenance et l'ajout d'un élément. Les sets ont des inconvénients dans d'autre situations, mais dans notre cas, ils sont la structure la plus adaptée.

### Question 3 : Quelle bibliothèque utilisez-vous pour lire les instructions des interrupteurs ? Dites en une ou deux phrases pourquoi vous avez choisi celle-là.

Nous avons choisi la bibliothèque pyymal pour la richesse de sa documentation, facilement accessible sur internet.

### Question 4 : Comment votre design général évolue-t-il pour tenir compte des interrupteurs et des portails ?

Nous avons changé la liste wall passée au physics_engine, pour qu'elle contienne les portes fermées en plus des murs.
Nous avons aussi dû modifier l'épée pour qu'elle se désactive immédiatement quand elle frappe un ennemi ou un interrupteur, afin d'éviter d'activer et de désactiver un interrupteur plusieurs fois à la suite, sans le vouloir.
Finalement, ayant mis en place la lecture de fichier avec YAML pour pouvoir lire la configuration des interrupteur, nous avons aussi pu en profiter pour intégrer la lecture des autres attributs (height, width et next-map) dans le YAML. Ainsi, toute notre configuration est maintenant lue grâce à YAML.