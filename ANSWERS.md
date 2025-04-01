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


### Question 2 (Paul) :



### Question 3 (Paul) :Où le remettez-vous à zéro ? Avez-vous du code dupliqué entre les cas où la joueuse perd parce qu’elle a touché un ou monstre ou de la lave ?
le score est initialiser en meme temps que la joueuse du coup il est remis a zero lors de l'inintialisation


### Question 4 (Paul)



### Question 5 (Gaëlle) : Comment modélisez-vous la “next-map” ? Où la stockez-vous, et comment la traitez-vous quand la joueuse atteint le point E ?

La next map est le chemin du prochain niveau, qui est stocké comme string dans un attribut de la class GameView. Cet attribut est mis à jour à chauque fois qu'une nouvelle map est crée par la méthode create_map(). Quand la joueuse atteint le point E, la méthode load_next_map() est appelée. Cette méthode s'assure que le nom de la prochaine map est bien stockée, puis remplace la map actuelle par la prochaine map dans l'attribut current_map_name, avant d'appeler la méthode setup qui crée le prochain niveau. 

### Question 6 (Gaëlle) : Que se passe-t-il si la joueuse atteint le E mais la carte n’a pas de next-map ?

Pour l'instant, ce cas de figure n'est pas possible. Si la carte a un "E" mais pas de next-map, la méthode create_map() appelé dès le début lèvera une exception. La map est ainsi considérée comme non-valide. On pourrait éventuellement considérer qu'arriver à la fin d'un niveau qui n'a pas de suite signifie que la joueuse a gagné le jeu, et afficher un message de victoire.

# Semaine 5

### Question 1 (Paul)

### Question 2 (Gaëlle)

### Question 3 (Paul)

### Question 4 (Paul et Gaëlle)