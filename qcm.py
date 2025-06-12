import streamlit as st
import random
import json
from datetime import datetime

# Configuration de la page
st.set_page_config(
    page_title="QCM Administration Avancée BDD",
    page_icon="🗄️",
    layout="wide"
)

# Initialisation du state
if 'current_question' not in st.session_state:
    st.session_state.current_question = 0
if 'score' not in st.session_state:
    st.session_state.score = 0
if 'answers' not in st.session_state:
    st.session_state.answers = []
if 'quiz_started' not in st.session_state:
    st.session_state.quiz_started = False
if 'quiz_finished' not in st.session_state:
    st.session_state.quiz_finished = False

# Base de questions du QCM
questions = [
    {
        "type": "mcq",
        "question": "Quelle est la taille par défaut d'un segment de journal des transactions (WAL) dans PostgreSQL ?",
        "options": ["8 Mo", "16 Mo", "32 Mo", "64 Mo"],
        "correct": 1,
        "explanation": "PostgreSQL organise le journal des transactions en segments de 16 Mo par défaut."
    },
    {
        "type": "multiple",
        "question": "Quels sont les niveaux de sécurité dans PostgreSQL ? (Plusieurs réponses possibles)",
        "options": [
            "Network authentication (pg_hba.conf)",
            "Instance-level permissions",
            "Database-level permissions",
            "Table-level permissions",
            "Column permissions"
        ],
        "correct": [0, 1, 2, 3, 4],
        "explanation": "PostgreSQL utilise 7 niveaux de sécurité : TCP on/off, Network auth, Instance, Database, Schema, Table, et Column permissions."
    },
    {
        "type": "code",
        "question": "Complétez cette commande pour créer un tablespace :",
        "code_template": "CREATE TABLESPACE mon_espace OWNER postgres _______ '/chemin/vers/le/dossier';",
        "correct": "LOCATION",
        "explanation": "La syntaxe correcte est : CREATE TABLESPACE mon_espace OWNER postgres LOCATION '/chemin/vers/le/dossier';"
    },
    {
        "type": "mcq",
        "question": "Quel est le but principal du journal des transactions (WAL) ?",
        "options": [
            "Améliorer les performances des requêtes",
            "Garantir qu'une instance DB puisse survivre aux pannes",
            "Stocker les données utilisateur",
            "Gérer les connexions utilisateur"
        ],
        "correct": 1,
        "explanation": "Le WAL (Write Ahead Log) garantit qu'une instance de base de données puisse survivre aux pannes en cas de crash du système."
    },
    {
        "type": "multiple",
        "question": "Quels sont les deux types de sauvegarde sous PostgreSQL ?",
        "options": [
            "Sauvegarde logique (SQL dump)",
            "Sauvegarde physique (File system level)",
            "Sauvegarde incrémentale",
            "Sauvegarde différentielle"
        ],
        "correct": [0, 1],
        "explanation": "PostgreSQL propose deux approches : sauvegarde logique (SQL dump) et sauvegarde physique (File system level backup)."
    },
    {
        "type": "code",
        "question": "Quelle commande permet de créer un utilisateur avec privilège de création de base de données ?",
        "code_template": "CREATE USER nom_utilisateur _______;",
        "correct": "CREATEDB",
        "explanation": "La commande correcte est : CREATE USER nom_utilisateur CREATEDB;"
    },
    {
        "type": "mcq",
        "question": "Quelle est la différence principale entre réplication synchrone et asynchrone ?",
        "options": [
            "La réplication synchrone est plus rapide",
            "La réplication asynchrone garantit la cohérence",
            "La réplication synchrone attend la confirmation avant de valider",
            "Il n'y a pas de différence"
        ],
        "correct": 2,
        "explanation": "En réplication synchrone, les transactions doivent être confirmées par tous les serveurs avant d'être validées, contrairement à l'asynchrone."
    },
    {
        "type": "multiple",
        "question": "Quels sont les avantages de l'internationalisation (i18n) dans PostgreSQL ?",
        "options": [
            "Support de l'encodage UTF-8",
            "Gestion des collations",
            "Formats de date et heure régionaux",
            "Messages d'erreur multilingues"
        ],
        "correct": [0, 1, 2, 3],
        "explanation": "PostgreSQL supporte l'i18n avec UTF-8, collations, formats régionaux et messages multilingues."
    },
    {
        "type": "code",
        "question": "Complétez la commande pour sauvegarder une base de données avec pg_dump :",
        "code_template": "pg_dump _______ > backup.sql",
        "correct": "dbname",
        "explanation": "La syntaxe correcte est : pg_dump dbname > backup.sql"
    },
    {
        "type": "mcq",
        "question": "Quel paramètre contrôle l'intervalle entre les checkpoints ?",
        "options": [
            "wal_level",
            "checkpoint_segments",
            "max_wal_senders",
            "archive_mode"
        ],
        "correct": 1,
        "explanation": "checkpoint_segments contrôle l'intervalle entre les checkpoints (par défaut 3 segments = 3 * 16 MB)."
    },
    {
        "type": "multiple",
        "question": "Quels sont les types de bases NoSQL mentionnés dans le cours ?",
        "options": [
            "Document (MongoDB)",
            "Clé-Valeur (Redis)",
            "Colonnes (Cassandra)",
            "Graphes (Neo4j)"
        ],
        "correct": [0, 1, 2, 3],
        "explanation": "Les 4 types principaux de NoSQL sont : Document, Clé-Valeur, Colonnes orientées, et Graphes."
    },
    {
        "type": "code",
        "question": "Complétez la commande pour accorder des privilèges SELECT à un utilisateur :",
        "code_template": "GRANT SELECT ON table_name __ user_name;",
        "correct": "TO",
        "explanation": "La syntaxe correcte est : GRANT SELECT ON table_name TO user_name;"
    },
{
        "type": "mcq",
        "question": "Quel processus est responsable de l'exécution de la tâche autovacuum dans PostgreSQL ?",
        "options": [
            "autovacuum launcher",
            "bgwriter",
            "checkpointer",
            "walwriter"
        ],
        "correct": 0,
        "explanation": "Le processus autovacuum launcher est chargé de lancer périodiquement les workers autovacuum pour nettoyer et analyser les tables."
    },
    {
        "type": "mcq",
        "question": "Quel paramètre configure les noms des serveurs standby synchrones dans PostgreSQL ?",
        "options": [
            "synchronous_commit",
            "synchronous_standby_names",
            "max_wal_senders",
            "wal_level"
        ],
        "correct": 1,
        "explanation": "synchronous_standby_names définit la liste des serveurs standby qui doivent confirmer l'écriture des WAL avant de valider une transaction en mode synchrone."
    },
    {
        "type": "mcq",
        "question": "Que signifie l'acronyme RPO en gestion de la reprise après sinistre ?",
        "options": [
            "Recovery Point Objective",
            "Recovery Performance Objective",
            "Restore Point Option",
            "Replication Process Optimization"
        ],
        "correct": 0,
        "explanation": "Le Recovery Point Objective (RPO) est le point dans le temps auquel on peut revenir après une panne, définissant la quantité maximale de données perdue acceptable."
    },
    {
        "type": "code",
        "question": "Complétez la commande pour activer l'extension FDW PostgreSQL :",
        "code_template": "CREATE EXTENSION ________;  ",
        "correct": "postgres_fdw",
        "explanation": "L'extension postgres_fdw est utilisée pour créer des Foreign Data Wrappers afin d'accéder à des tables distantes."
    },
    {
        "type": "code",
        "question": "Complétez la commande pour ajouter un utilisateur à un groupe :",
        "code_template": "ALTER GROUP nom_groupe ________ nom_utilisateur;",
        "correct": "ADD USER",
        "explanation": "La syntaxe ALTER GROUP nom_groupe ADD USER nom_utilisateur permet d'ajouter un utilisateur au groupe."
    },
    {
        "type": "code",
        "question": "Complétez la commande pg_dump pour se connecter à un serveur distant avec authentification :",
        "code_template": "pg_dump -h host -p port -U ________ dbname > backup.sql",
        "correct": "nom_utilisateur",
        "explanation": "Le paramètre -U est suivi du nom d'utilisateur pour l'authentification lors de l'utilisation de pg_dump."
    },
    {
        "type": "multiple",
        "question": "Quelles sont les fonctionnalités prises en charge par le Write-Ahead Log (WAL) ?",
        "options": [
            "Durabilité des transactions",
            "Réplication vers les standbys",
            "Optimisation des requêtes SELECT",
            "Recovery Point-in-Time (PITR)",
            "Gestion des verrous"
        ],
        "correct": [0, 1, 3],
        "explanation": "Le WAL assure la durabilité des transactions, le support de la réplication et permet le point-in-time recovery, mais n'optimise pas directement les requêtes ni gère les verrous."
    },
    {
        "type": "multiple",
        "question": "Selon le théorème CAP, quelles sont les trois garanties que tout système distribué ne peut satisfaire simultanément ?",
        "options": [
            "Cohérence (Consistency)",
            "Haute disponibilité (Availability)",
            "Tolérance au partitionnement (Partition Tolerance)",
            "Durabilité (Durability)",
            "Scalabilité (Scalability)"
        ],
        "correct": [0, 1, 2],
        "explanation": "Le théorème CAP stipule qu'un système distribué ne peut simultanément garantir la cohérence, la disponibilité et la tolérance aux partitions."
    },
    {
        "type": "mcq",
        "question": "Quel catalogue système stocke les informations sur les tablespaces dans PostgreSQL ?",
        "options": [
            "pg_tablespace",
            "pg_database",
            "pg_class",
            "pg_tables"
        ],
        "correct": 0,
        "explanation": "Le catalogue pg_tablespace contient les métadonnées sur les tablespaces définis dans un cluster PostgreSQL."
    }
]


def shuffle_questions():
    """Mélange les questions pour chaque session"""
    random.shuffle(questions)


def display_question(q_index):
    """Affiche une question selon son type"""
    if q_index >= len(questions):
        return None

    question = questions[q_index]
    st.write(f"**Question {q_index + 1}/{len(questions)}**")
    st.write(question["question"])

    if question["type"] == "mcq":
        return st.radio("Choisissez votre réponse:", question["options"], key=f"q_{q_index}")

    elif question["type"] == "multiple":
        st.write("*Plusieurs réponses possibles*")
        selected = []
        for i, option in enumerate(question["options"]):
            if st.checkbox(option, key=f"q_{q_index}_{i}"):
                selected.append(i)
        return selected

    elif question["type"] == "code":
        st.code(question["code_template"], language="sql")
        return st.text_input("Complétez le code:", key=f"q_{q_index}")


def check_answer(q_index, user_answer):
    """Vérifie si la réponse est correcte"""
    question = questions[q_index]

    if question["type"] == "mcq":
        return user_answer == question["correct"]

    elif question["type"] == "multiple":
        return set(user_answer) == set(question["correct"])

    elif question["type"] == "code":
        return user_answer.upper().strip() == question["correct"].upper()


def main():
    st.title("🗄️ QCM Administration Avancée de Bases de Données")
    st.subheader("Cours L3 - IUT Informatique Belfort")

    # Sidebar avec informations
    with st.sidebar:
        st.header("📊 Informations")
        if st.session_state.quiz_started:
            st.metric("Question actuelle", f"{st.session_state.current_question + 1}/{len(questions)}")
            st.metric("Score actuel",
                      f"{st.session_state.score}/{st.session_state.current_question + 1}" if st.session_state.current_question > 0 else "0/0")
            progress = (st.session_state.current_question + 1) / len(questions)
            st.progress(progress)

        st.markdown("---")
        st.markdown("**Thèmes couverts :**")
        st.markdown("""
        - 🗂️ Gestion des espaces de données
        - 👥 Gestion des utilisateurs  
        - 💾 Backup/Restore
        - 🔄 Réplication
        - 🌐 Fédération
        - 🌍 Internationalisation
        - 📈 Types de bases de données
        """)

    # Page d'accueil
    if not st.session_state.quiz_started:
        st.markdown("""
        ### Bienvenue dans votre QCM de révision !

        Ce quiz contient **12 questions** sur les concepts avancés d'administration de bases de données :

        - **Questions à choix multiples** (QCM classiques)
        - **Questions à choix multiples** (plusieurs réponses possibles)  
        - **Questions de code** (compléter des commandes SQL)

        Cliquez sur le bouton ci-dessous pour commencer !
        """)

        col1, col2, col3 = st.columns([1, 1, 1])
        with col2:
            if st.button("🚀 Commencer le QCM", size="large"):
                shuffle_questions()
                st.session_state.quiz_started = True
                st.session_state.current_question = 0
                st.session_state.score = 0
                st.session_state.answers = []
                st.rerun()

    # Quiz en cours
    elif st.session_state.quiz_started and not st.session_state.quiz_finished:
        current_q = st.session_state.current_question

        if current_q < len(questions):
            user_answer = display_question(current_q)

            col1, col2 = st.columns([1, 1])

            with col1:
                if st.button("⬅️ Question précédente", disabled=current_q == 0):
                    if current_q > 0:
                        st.session_state.current_question -= 1
                        st.rerun()

            with col2:
                if current_q == len(questions) - 1:
                    if st.button("🏁 Terminer le QCM"):
                        if user_answer is not None:
                            is_correct = check_answer(current_q, user_answer)
                            st.session_state.answers.append({
                                'question': questions[current_q]["question"],
                                'user_answer': user_answer,
                                'correct': is_correct,
                                'explanation': questions[current_q]["explanation"]
                            })
                            if is_correct:
                                st.session_state.score += 1
                            st.session_state.quiz_finished = True
                            st.rerun()
                else:
                    if st.button("➡️ Question suivante"):
                        if user_answer is not None:
                            is_correct = check_answer(current_q, user_answer)
                            st.session_state.answers.append({
                                'question': questions[current_q]["question"],
                                'user_answer': user_answer,
                                'correct': is_correct,
                                'explanation': questions[current_q]["explanation"]
                            })
                            if is_correct:
                                st.session_state.score += 1
                            st.session_state.current_question += 1
                            st.rerun()

    # Résultats finaux
    else:
        st.balloons()

        score_percentage = (st.session_state.score / len(questions)) * 100

        st.markdown(f"""
        ## 🎉 QCM Terminé !

        ### Votre score : {st.session_state.score}/{len(questions)} ({score_percentage:.1f}%)
        """)

        # Affichage du niveau
        if score_percentage >= 80:
            st.success("🏆 Excellent ! Vous maîtrisez parfaitement le cours !")
        elif score_percentage >= 60:
            st.info("👍 Bien ! Quelques révisions et ce sera parfait !")
        else:
            st.warning("📚 Il faut réviser ! Relisez le cours attentivement.")

        # Détail des réponses
        st.markdown("### 📋 Détail de vos réponses")

        for i, answer in enumerate(st.session_state.answers):
            with st.expander(f"Question {i + 1} - {'✅ Correct' if answer['correct'] else '❌ Incorrect'}"):
                st.write(f"**Question :** {answer['question']}")
                st.write(f"**Votre réponse :** {answer['user_answer']}")
                st.info(f"**Explication :** {answer['explanation']}")

        # Bouton recommencer
        col1, col2, col3 = st.columns([1, 1, 1])
        with col2:
            if st.button("🔄 Recommencer le QCM"):
                st.session_state.quiz_started = False
                st.session_state.quiz_finished = False
                st.session_state.current_question = 0
                st.session_state.score = 0
                st.session_state.answers = []
                st.rerun()


if __name__ == "__main__":
    main()