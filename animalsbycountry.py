# -*- coding: utf-8 -*-
"""
Created on Wed Dec 18 08:14:25 2019

@author: Lawsky
"""

animals_by_country_dict = {'English':['Canidae', 'Felidae', 'Cat', 'Cattle', 'Dog', 'Donkey', 'Goat', 'Guinea Pig', 'Horse', 'Pig', 'Rabbit', 'Fancy Rat Varieties', 'Laboratory Rat Strains', 'Sheep Breeds', 'Water Buffalo Breeds', 'Chicken Breeds', 'Duck Breeds', 'Goose Breeds', 'Pigeon Breeds', 'Turkey Breeds', 'Aardvark', 'Aardwolf', 'African Buffalo', 'African Elephant', 'African Leopard', 'Albatross', 'Alligator', 'Alpaca', 'American Robin', 'Amphibian', 'Anaconda', 'Angelfish', 'Anglerfish', 'Ant', 'Anteater', 'Antelope', 'Antlion', 'Ape', 'Aphid', 'Arabian Leopard', 'Arctic Fox', 'Arctic Wolf', 'Armadillo', 'Arrow Crab', 'Asp', 'Baboon', 'Badger', 'Bald Eagle', 'Bandicoot', 'Barnacle', 'Barracuda', 'Basilisk', 'Bass', 'Bat', 'Beaked Whale', 'Bear', 'Beaver', 'Bee', 'Beetle', 'Bird', 'Bison', 'Blackbird', 'Black Panther', 'Black Widow Spider', 'Blue Bird', 'Blue Jay', 'Blue Whale', 'Boa', 'Boar', 'Bobcat', 'Bobolink', 'Bonobo', 'Booby', 'Box Jellyfish', 'Bovid', 'Bug', 'Butterfly', 'Buzzard', 'Camel', 'Canid', 'Cape Buffalo', 'Capybara', 'Cardinal', 'Caribou', 'Carp', 'Cat', 'Catshark', 'Caterpillar', 'Catfish', 'Cattle', 'Centipede', 'Cephalopod', 'Chameleon', 'Cheetah', 'Chickadee', 'Chicken', 'Chimpanzee', 'Chinchilla', 'Chipmunk', 'Clam', 'Clownfish', 'Cobra', 'Cockroach', 'Cod', 'Condor', 'Constrictor', 'Coral', 'Cougar', 'Cow', 'Coyote', 'Crab', 'Crane', 'Crane Fly', 'Crawdad', 'Crayfish', 'Cricket', 'Crocodile', 'Crow', 'Cuckoo', 'Cicada', 'Damselfly', 'Deer', 'Dingo', 'Dinosaur', 'Dog', 'Dolphin', 'Donkey', 'Dormouse', 'Dove', 'Dragonfly', 'Dragon', 'Duck', 'Dung Beetle', 'Eagle', 'Earthworm', 'Earwig', 'Echidna', 'Eel', 'Egret', 'Elephant', 'Elephant Seal', 'Elk', 'Emu', 'English Pointer', 'Ermine', 'Falcon', 'Ferret', 'Finch', 'Firefly', 'Fish', 'Flamingo', 'Flea', 'Fly', 'Flyingfish', 'Fowl', 'Fox', 'Frog', 'Fruit Bat', 'Gamefowl', 'Galliform', 'Gazelle', 'Gecko', 'Gerbil', 'Giant Panda', 'Giant Squid', 'Gibbon', 'Gila Monster', 'Giraffe', 'Goat', 'Goldfish', 'Goose', 'Gopher', 'Gorilla', 'Grasshopper', 'Great Blue Heron', 'Great White Shark', 'Grizzly Bear', 'Ground Shark', 'Ground Sloth', 'Grouse', 'Guan', 'Guanaco', 'Guineafowl', 'Guinea Pig', 'Gull', 'Guppy', 'Haddock', 'Halibut', 'Hammerhead Shark', 'Hamster', 'Hare', 'Harrier', 'Hawk', 'Hedgehog', 'Hermit Crab', 'Heron', 'Herring', 'Hippopotamus', 'Hookworm', 'Hornet', 'Horse', 'Hoverfly', 'Hummingbird', 'Humpback Whale', 'Hyena', 'Iguana', 'Impala', 'Irukandji Jellyfish', 'Jackal', 'Jaguar', 'Jay', 'Jellyfish', 'Junglefowl', 'Kangaroo', 'Kangaroo Mouse', 'Kangaroo Rat', 'Kingfisher', 'Kite', 'Kiwi', 'Koala', 'Koi', 'Komodo Dragon', 'Krill', 'Ladybug', 'Lamprey', 'Landfowl', 'Land Snail', 'Lark', 'Leech', 'Lemming', 'Lemur', 'Leopard', 'Leopon', 'Limpet', 'Lion', 'Lizard', 'Llama', 'Lobster', 'Locust', 'Loon', 'Louse', 'Lungfish', 'Lynx', 'Macaw', 'Mackerel', 'Magpie', 'Mammal', 'Manatee', 'Mandrill', 'Manta Ray', 'Marlin', 'Marmoset', 'Marmot', 'Marsupial', 'Marten', 'Mastodon', 'Meadowlark', 'Meerkat', 'Mink', 'Minnow', 'Mite', 'Mockingbird', 'Mole', 'Mollusk', 'Mongoose', 'Monitor Lizard', 'Monkey', 'Moose', 'Mosquito', 'Moth', 'Mountain Goat', 'Mouse', 'Mule', 'Muskox', 'Narwhal', 'Newt', 'New World Quail', 'Nightingale', 'Ocelot', 'Octopus', 'Old World Quail', 'Opossum', 'Orangutan', 'Orca', 'Ostrich', 'Otter', 'Owl', 'Ox', 'Panda', 'Panther', 'Panthera Hybrid', 'Parakeet', 'Parrot', 'Parrotfish', 'Partridge', 'Peacock', 'Peafowl', 'Pelican', 'Penguin', 'Perch', 'Peregrine Falcon', 'Pheasant', 'Pig', 'Pigeon', 'Pike', 'Pilot Whale', 'Pinniped', 'Piranha', 'Planarian', 'Platypus', 'Polar Bear', 'Pony', 'Porcupine', 'Porpoise', "Portuguese Man O' War", 'Possum', 'Prairie Dog', 'Prawn', 'Praying Mantis', 'Primate', 'Ptarmigan', 'Puffin', 'Puma', 'Python', 'Quail', 'Quelea', 'Quokka', 'Rabbit', 'Raccoon', 'Rainbow Trout', 'Rat', 'Rattlesnake', 'Raven', 'Red Panda', 'Reindeer', 'Reptile', 'Rhinoceros', 'Right Whale', 'Roadrunner', 'Rodent', 'Rook', 'Rooster', 'Roundworm', 'Saber-Toothed Cat', 'Sailfish', 'Salamander', 'Salmon', 'Sawfish', 'Scale Insect', 'Scallop', 'Scorpion', 'Seahorse', 'Sea Lion', 'Sea Slug', 'Sea Snail', 'Shark', 'Sheep', 'Shrew', 'Shrimp', 'Silkworm', 'Silverfish', 'Skink', 'Skunk', 'Sloth', 'Slug', 'Smelt', 'Snail', 'Snake', 'Snipe', 'Snow Leopard', 'Sockeye Salmon', 'Sole', 'Sparrow', 'Sperm Whale', 'Spider', 'Spider Monkey', 'Spoonbill', 'Squid', 'Squirrel', 'Starfish', 'Star-Nosed Mole', 'Steelhead Trout', 'Stingray', 'Stoat', 'Stork', 'Sturgeon', 'Sugar Glider', 'Swallow', 'Swan', 'Swift', 'Swordfish', 'Swordtail', 'Tahr', 'Takin', 'Tapir', 'Tarantula', 'Tarsier', 'Tasmanian Devil', 'Termite', 'Tern', 'Thrush', 'Tiger', 'Tiger Shark', 'Tiglon', 'Toad', 'Tortoise', 'Toucan', 'Trapdoor Spider', 'Tree Frog', 'Trout', 'Tuna', 'Turkey', 'Turtle', 'Tyrannosaurus', 'Urial', 'Vampire Bat', 'Vampire Squid', 'Vicuna', 'Viper', 'Vole', 'Vulture', 'Wallaby', 'Walrus', 'Wasp', 'Warbler', 'Water Boa', 'Water Buffalo', 'Weasel', 'Whale', 'Whippet', 'Whitefish', 'Whooping Crane', 'Wildcat', 'Wildebeest', 'Wildfowl', 'Wolf', 'Wolverine', 'Wombat', 'Woodpecker', 'Worm', 'Wren', 'Xerinae', 'X-Ray Fish', 'Yak', 'Yellow Perch', 'Zebra', 'Zebra Finch', 'Alpaca', 'Bali Cattle', 'Cat', 'Cattle', 'Chicken', 'Dog', 'Domestic Bactrian Camel', 'Domestic Canary', 'Domestic Dromedary Camel', 'Domestic Duck', 'Domestic Goat', 'Domestic Goose', 'Domestic Guineafowl', 'Domestic Hedgehog', 'Domestic Pig', 'Domestic Pigeon', 'Domestic Rabbit', 'Domestic Silkmoth', 'Domestic Silver Fox', 'Domestic Turkey', 'Donkey', 'Fancy Mouse', 'Fancy Rat', 'Lab Rat', 'Ferret', 'Gayal', 'Goldfish', 'Guinea Pig', 'Guppy', 'Horse', 'Koi', 'Llama', 'Ringneck Dove', 'Sheep', 'Siamese Fighting Fish', 'Society Finch', 'Yak', 'Water Buffalo'],
 'French':['Le Taureau', 'Les Bovins', 'Le Poulet', 'La Vache', 'Le Canard', 'Le Caneton', "L'Oie", 'La Poule', 'Le Cheval', "L'Agneau", 'Le Lama', 'La Souris', 'La Mule', "L'Autruche", 'Le Cochon', 'Le Poney', 'La Renne', 'Le Coq', 'Le Mouton', "Les Buffles D'Eau", 'Le Chat', 'Le Chien', 'Le Furet', 'Le Poisson Rouge', 'La Gerbille', "Le Cochon D'Inde", 'Le Hamster', 'Le Chaton', 'La Perruche', 'Le Perroquet', 'Le Choit', "L'Antilope", 'Le Blaireau', 'La Chauve-Souris', "L'Ours", 'Le Castor', "L'Oiseau", 'Les Oiseaux', 'Le Tamia', 'Le Cerf', 'Le Renard', "L'Orignal", 'La Loutre', 'Le Hibou', 'Le Lapin', 'Le Raton-Laveur', 'Le Loup', 'La Fourmi', "L'Abeille", 'Le Papillon', 'La Chenille', 'Le Cafard', 'Le Criquet', 'La Luciole', 'La Sauterelle', 'La Coccinelle', 'La Moustique', 'La Mante Religieuse', "L'Escargot", 'Le Ver'],
 'German':['Der Hund', 'Der Welpe', 'Die Katze', 'Der Kater', 'Das Kaninchen', 'Der Fisch', 'Der Hamster', 'Das Meerschweinchen', 'Die Schlange', 'Der Vogel', 'Der Papagei', 'Die Eidechse', 'Die Maus', 'Der Gecko', 'Das Huhn', 'Die Kuh', 'Das Schwein', 'Das Schaf', 'Das Lamm', 'Die Ziege', 'Das Pferd', 'Der Esel', 'Die Ente', 'Der Hase', 'Die Biene', 'Die Spinne', 'Der Wolf', 'Das Frettchen', 'Die Fledermaus', 'Der Igel', 'Der Otter', 'Der Elch', 'Die Spitzmaus', 'Das Wildschwein', 'Die Giraffe', 'Der Tiger', 'Der Elefant', 'Das Zebra', 'Der Leopard', 'Der Panther', 'Der Affe', 'Der Gepard', 'Die Antilope', 'Das Flusspferd', 'Der Pavian', 'Das Nashorn', 'Der Gorilla', 'Das Warzenschwein', 'Der Mungo', 'Das Kamel', 'Das Erdferkel', 'Die Ameise', 'Die Biene', 'Die Wespe', 'Die Hornisse', 'Die Qualle', 'Der Skorpion', 'Die Giftschlange', 'Die Spinne', 'Die Zecke', 'Der Moskito', 'Die Bremse', 'Die Bettwanze', 'Der Wal', 'Der Hai', 'Die Robbe', 'Das Walross', 'Der Delfin', 'Die Krabbe', 'Der Hummer', 'Die Garnele', 'Der Seestern', 'Der Seeigel', 'Der Tintenfisch', 'Der Stachelrochen', 'Der Pinguin', 'Der Schneeleopard', 'Der Narwal', 'Das Karibu', 'Die Taube', 'Die Elster', 'Der Spatz', 'Die Schwalbe', 'Die Amsel', 'Die Eule', 'Die Gans', 'Der Falke', 'Der Wellensittich', 'Der Geier', 'Der Pfau', 'Die Kaulquappe', 'Der Karpfen', 'Der Wassermolch'],
 'Dutch':['De Koe', 'De Stier', 'De Vaars', 'Het Kalf', 'Het Schaap', 'De Ram', 'De Ooi', 'Het Lam', 'De Geit', 'Het Geitje', 'Het Varken', 'Het Varkentje', 'Het Paard', 'De Hengst', 'De Merrie', 'Het Veulen', 'De Pony', 'De Shetland Pony', 'Het Engelse Trekpaard', 'De Ezel', 'De Muilezel', 'De Zebra', 'Het Stinkdier', 'De Wasbeer', 'De Mangoeste', 'Het Gordeldier', 'Het Aardvarken', 'De Tapir', 'De Beer', 'De Ijsbeer', 'De Poolvos', 'De Piranha', 'Het Hert', 'De Hertenbok', 'Het Hert', 'De Eland', 'De Antilope', 'De Eland', 'De Impala', 'Het Rendier', 'De Kariboe', 'De Steenbok', 'Het Wildebeest', 'De Aap', 'De Chimpansee', 'De Gorilla', 'Het Luipaard', 'De Oerang-Oetang', 'De Baviaan', 'De Wombat', 'De Koala Beer', 'De Wallaby', 'De Kangoeroe', 'De Haas', 'De Vos', 'De Wezel', 'De Das', 'De Vleermuis', 'De Fruitvleermuis', 'De Mol', 'De Hermelijn', 'De Egel', 'De Slak', 'De Naaktslak', 'De Slang', 'De Cobra', 'De Ratelslang', 'De Koraalslang', 'De Anaconda', 'De Boa Constrictor', 'De Python', 'De Hagedis', 'De Iguana', 'De Komodovaraan', 'De Waterschildpad', 'De Panda', 'De Olifant', 'De Mannetjesolifant', 'De Vrouwtjesolifant', 'De Giraf', 'De Hyena', 'De Jakhals', 'De Wolf', 'De Buffel', 'De Bizon', 'De Neushoorn', 'De Krokodil', 'De Alligator', 'Het Nijlpaard', 'De Walrus', 'De Lamantijn', 'Het Vogelbekdier', 'De Kameel', 'De Dromedaris', 'De Lama', 'De Jak'],
 'Spanish':['El Perro', 'El Cachorro', 'El Gato', 'La Cobaya', 'El Pez', 'El Perico', 'La Tortuga', 'La Serpiente', 'El Conejo', 'El Pollo', 'La Gallina', 'El Gallo', 'La Vaca', 'El Toro', 'La Oveja', 'El Caballo', 'El Cerdo', 'La Cabra', 'El Burro', 'El Ciervo', 'El Mapache', 'La Ardilla', 'El Zorro', 'El Lobo', 'El Oso', 'El Cangrejo', 'El Aguaviva', 'La Ballena', 'La Foca', 'El Lobo Marino', 'La Morsa', 'El Elefante', 'El Rinoceronte', 'El Tigre', 'La Jirafa', 'La Cebra', 'El Mono', 'El Canguro', 'El Cocodrilo', 'La Oruga', 'La Mariposa', 'La Polilla', 'La Mosca', 'La Cucaracha', 'El Caracol', 'El Gusano'],
 'Portugese':['Formiga', 'Tatu', 'Jumento', 'Morcego', 'Urso', 'Abelha', 'Besouro', 'Javali', 'Touro', 'Borboleta', 'Camelo', 'Gato', 'Frango', 'Barata', 'Bacalhau', 'Coral', 'Vaca', 'Caranguejo', 'Siri', 'Grilo', 'Crocodilo', 'Veado', 'Dinossauro', 'Cachorro', 'Burro', 'Pombo', 'Pato', 'Minhoca', 'Enguia', 'Elefante', 'Vaga-Lume', 'Peixe', 'Flamingo', 'Pulga', 'Mosca', 'Raposa', 'Girafa', 'Cabra', 'Bode', 'Ganso', 'Gorila', 'Gafanhoto', 'Galinha', 'Cavalo', 'Beija-Flor', 'Hiena', 'Canguru', 'Orca', 'Koala', 'Joaninha', 'Cordeiro', 'Sanguessuga', 'Leopardo', 'Lagosta', 'Piolho', 'Arara', 'Macaco', 'Alce', 'Mosquito', 'Pernilongo', 'Camundongo', 'Polvo', 'Avestruz', 'Coruja', 'Boi', 'Ostra', 'Panda', 'Pantera', 'Papagaio', 'Pelicano', 'Pinguim', 'Porco', 'Urso Polar', 'Codorna', 'Coelho', 'Rato', 'Arraia', 'Raia', 'Rinoceronte', 'Galo', 'Sardinha',  'Gaivota', 'Foca', 'Ovelha', 'Carneiro', 'Lesma', 'Cobra', 'Serpente', 'Aranha', 'Esponja', 'Lula', 'Esquilo', 'Cegonha', 'Cisne', 'Cupim', 'Tigre', 'Sapo', 'Truta', 'Atum', 'Peru', 'Tartaruga', 'Vespa', 'Baleia', 'Lobo', 'Zebra']}