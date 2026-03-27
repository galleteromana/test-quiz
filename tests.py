import pytest
from model import Question


def test_create_question():
    question = Question(title='q1')
    assert question.id != None

def test_create_multiple_questions():
    question1 = Question(title='q1')
    question2 = Question(title='q2')
    assert question1.id != question2.id

def test_create_question_with_invalid_title():
    with pytest.raises(Exception):
        Question(title='')
    with pytest.raises(Exception):
        Question(title='a'*201)
    with pytest.raises(Exception):
        Question(title='a'*500)

def test_create_question_with_valid_points():
    question = Question(title='q1', points=1)
    assert question.points == 1
    question = Question(title='q1', points=100)
    assert question.points == 100

def test_create_choice():
    question = Question(title='q1')
    
    question.add_choice('a', False)

    choice = question.choices[0]
    assert len(question.choices) == 1
    assert choice.text == 'a'
    assert not choice.is_correct

#-----------------------------------------

from model import Choice

# 1. Testa auto-incremento de IDs das escolhas
def test_choices_should_have_incremental_ids():
    question = Question(title="Qual a capital do Brasil?")
    choice1 = question.add_choice("Rio de Janeiro")
    choice2 = question.add_choice("Brasília")
    
    assert choice1.id == 1
    assert choice2.id == 2

# 2. Validação de pontos fora do intervalo
def test_question_points_should_be_between_one_and_hundred():
    with pytest.raises(Exception, match="Points must be between 1 and 100"):
        Question(title="Título", points=0)
    with pytest.raises(Exception, match="Points must be between 1 and 100"):
        Question(title="Título", points=101)

# 3. Validação de tamanho de texto na Choice
def test_choice_text_constraints():
    question = Question(title="Título")
    with pytest.raises(Exception, match="Text cannot be empty"):
        question.add_choice("")
    with pytest.raises(Exception, match="Text cannot be longer than 100 characters"):
        question.add_choice("a" * 101)

# 4. Remoção individual de uma escolha
def test_remove_single_choice_by_id():
    question = Question(title="Título")
    c1 = question.add_choice("Opção 1")
    question.add_choice("Opção 2")
    
    question.remove_choice_by_id(c1.id)
    
    assert len(question.choices) == 1
    assert question.choices[0].text == "Opção 2"

# 5. Comportamento ao tentar remover um ID inexistente
def test_remove_invalid_choice_id_should_raise_exception():
    question = Question(title="Título")
    question.add_choice("Opção 1")
    
    with pytest.raises(Exception, match="Invalid choice id 99"):
        question.remove_choice_by_id(99)

# 6. Funcionalidade de limpar todas as escolhas
def test_remove_all_choices_behavior():
    question = Question(title="Título")
    question.add_choice("A")
    question.add_choice("B")
    
    question.remove_all_choices()
    
    assert len(question.choices) == 0

# 7. Atualização de respostas corretas em lote
def test_set_correct_choices_updates_multiple_statuses():
    question = Question(title="Quais são cores?")
    c1 = question.add_choice("Azul", is_correct=False)
    c2 = question.add_choice("Carro", is_correct=False)
    c3 = question.add_choice("Verde", is_correct=False)
    
    question.set_correct_choices([c1.id, c3.id])
    
    assert c1.is_correct is True
    assert c2.is_correct is False
    assert c3.is_correct is True

# 8. Correção de escolhas selecionadas
def test_correct_selected_choices_returns_only_right_answers():
    question = Question(title="Capital", max_selections=2)
    c1 = question.add_choice("Brasília", is_correct=True)
    c2 = question.add_choice("Lisboa", is_correct=False)
    
    correct_ids = question.correct_selected_choices([c1.id, c2.id])
    
    assert len(correct_ids) == 1
    assert c1.id in correct_ids

# 9. Restrição de limite máximo de seleções
def test_correction_should_fail_if_selections_exceed_max_limit():
    question = Question(title="Escolha uma", max_selections=1)
    c1 = question.add_choice("A")
    c2 = question.add_choice("B")
    
    with pytest.raises(Exception, match="Cannot select more than 1 choices"):
        question.correct_selected_choices([c1.id, c2.id])

# 10. Testa se IDs de escolha são preservados após remoções e novas adições
def test_choice_id_continuity_after_removal():
    question = Question(title="ID Test")
    c1 = question.add_choice("Primeira") # ID 1
    c2 = question.add_choice("Segunda")  # ID 2
    
    question.remove_choice_by_id(c1.id)
    c3 = question.add_choice("Terceira") # Deve pegar o ID do último (2) + 1
    
    assert c3.id == 3