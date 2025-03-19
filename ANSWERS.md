## Semaine 3

### Question 1 : Comment avez-vous conçu la lecture du fichier ? Comment l’avez-vous structurée de sorte à pouvoir la tester de manière efficace ?

La lecture du fichier se fait à travers la méthode create_map() de la classe GameView. Cette méthode est appelée par setup(), d'où elle tire également l'emplacement du fichier qu'elle doit lire. 
Elle vérifie que le fichier ait un format valable au fil et à mesure de la lecture. Si le fichier n'a pas la bonne structure, la méthode envoie une exception. 
Ainsi, la méthode est testée en créant une instance de GameView avec comme argument différents fichiers tests, certains valables et d'autre pas. Les fichier non-valables sont testés en vérifiant que la méthode renvoie bien la bonne exception, et stockés dans le dossier "maps/bad_maps".
main() s'occupe ensuite des exceptions lancées par create_map(), en imprimant l'exception dans la console.


### Question 2 : Comment avez-vous adapté vos tests existants au fait que la carte ne soit plus la même qu’au départ ? Est-ce que vos tests résisteront à d’autres changements dans le futur ? Si oui, pourquoi ? Si non, que pensez-vous faire plus tard ?

Nous avons recrée la map de départ dans un fichier nommé "default_map.txt". Le chemin de ce fichier est passé par défaut à GameView, si aucun autre argument n'est donné pour le chemin de la map. Les tests existants n'ont alors pas dû être modifiés. On aurait aussi pu simplement passer le chemin de cette map à tous les tests déjà écrits. Il se peut que nous fassions cela plus tard, s'il pour une raison quelconque nous devons changer la map proposée par defaut. Nous ne voyons pas de raison pour laquelle les tests ne résisteraient pas à d'autres changements (raisonnables) dans le futur, surtout si la méthode de passer la map à GameView ne change pas. Il sera à priori toujours possible de choisir quel map utiliser pour chaque test individuellement.

### Question 3 : Le code qui gère la lave ressemble-t-il plus à celui de l’herbe, des pièces, ou des blobs ? Expliquez votre réponse.
Le code qui gere la lave resemble au code qui gere les colision avec les blob car il fais pratiquement la meme chose (tue la joueuse et recomence instantanement le le niveau)




### Question 4 : Comment détectez-vous les conditions dans lesquelles les blobs doivent changer de direction ?
cette partie resemble beaucoup a celle de la gestion du saut de la joueuse dans arcade (un abaisement temporaire de la position puis un check de colision avec un mur et une remise a la position initiale) j'ai juste ajouter un deplacement selon y dans le sens d'avancement du slime