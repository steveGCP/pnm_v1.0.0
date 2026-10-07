from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import authenticate, login as auth_login, logout
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from .forms import ProjectForm
from .models import Project, MatchResult
import urllib.request
import json


# Create your views here.

def signUp(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save() #Enregistre l'utilisateur et hache le mot de passe
            auth_login(request, user)

            return redirect('dashboard') #Redirige vers la page de connexion
    else:
        form = UserCreationForm()
    return render(request, 'signUp.html', {'form': form})


def login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            #Récupère l'utilisateur
            user = form.get_user()
            auth_login(request, user)
            return redirect('dashboard')
    else: 
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})


@login_required
def dashboard(request):
    #Cherche si l'utilisateur a déjà un projet, si non renvoie None
    try:
        project = request.user.project
    except Project.DoesNotExist:
        project = None

    if request.method == 'POST':
        #On lie le formulaire aux données envoyées et au projet existant s'il y en a un
        form = ProjectForm(request.POST, instance=project)
        if form.is_valid():
            new_project = form.save(commit=False)
            new_project.user = request.user
            new_project.save()
            # Lancer le matching automatiquement
            run_matching_for_project(new_project)
            return redirect('dashboard')
    else:
        #Si le projet n'existe pas, on crée un formulaire vide
        form = ProjectForm(instance=project)

    # Récupérer les 5 meilleurs matchs pour le projet de l'utilisateur
    if project:
        matches = MatchResult.objects.filter(Q(project1=project) | Q(project2=project)).order_by('-score')[:5]
    else:
        matches = []
        
    return render(request, 'dashboard.html', {'form': form, 'matches': matches})

def run_matching_for_project(my_project):
    """
    Fonction utilitaire pour comparer un projet avec tous les autres 
    et sauvegarder les résultats dans MatchResult.
    """
    other_projects = Project.objects.exclude(user=my_project.user)

    for other_p in other_projects:
        prompt = f"""
        tu es un expert en startup et co-fondation.
        Projet 1 : {my_project.pitch}
        Projet 2 : {other_p.pitch}
        Analyse la compatibilité entre ces 2 projets pour une potentielle collaboration.
        Réponds Uniquement avec un format JSON strict contenant deux clés : "score" (un nombre entre 0 et 100)
        et "explanation" (un texte explicatif court).
        Exemple de réponse attendue : {{"score" : 85, "explanation" : "Les deux projets sont complémentaires"}}
        """
        
        data = json.dumps({
            "model": "gemma2:9b", 
            "prompt": prompt, 
            "stream": False, 
            "format": "json"
        }).encode('utf-8')

        req = urllib.request.Request(
            'http://localhost:11434/api/generate', 
            data=data, 
            headers={'content-Type': 'application/json'}
        )

        try: 
            with urllib.request.urlopen(req) as response:
                response_body = json.loads(response.read().decode('utf-8'))
                
                # Nettoyage en cas de balises markdown résiduelles
                text_response = response_body['response'].replace('```json', '').replace('```', '').strip()
                ia_response = json.loads(text_response)

                score = int(ia_response.get('score') or 0)
                explanation = ia_response.get('explanation', "Pas d'explication fournie.")

                # Mettre à jour ou créer le match (dans un sens ou l'autre)
                match, created = MatchResult.objects.get_or_create(
                    project1=min(my_project, other_p, key=lambda p: p.id),
                    project2=max(my_project, other_p, key=lambda p: p.id),
                    defaults={'score': score, 'explanation': explanation}
                )
                
                if not created:
                    match.score = score
                    match.explanation = explanation
                    match.save()

        except Exception as e:
            print(f"Erreur lors de la comparaison avec {other_p.name} : {e}")
            continue

# La vue start_matching est maintenant obsolète puisque c'est fait automatiquement !
# Je la laisse vide avec une simple redirection vers le dashboard au cas où l'utilisateur y accèderait directement.
@login_required
def start_matching(request):
    return redirect('dashboard')



def index(request): 
    return render(request, "index.html")

def logout_view(request):
    logout(request)
    return redirect('index')