from django.shortcuts import render
from django.http import JsonResponse
from django import forms
from transformers import pipeline

sentiment_model = pipeline("text-classification", model="Gnider/robertabase_sentim_analys")
rating_model = pipeline("text-classification", model="Gnider/robertabase_rating_analys")

class TextInputForm(forms.Form):
    text = forms.CharField(widget=forms.Textarea, label='Enter text for classification')

def analyze_text(request):
    if request.method == 'POST':
        form = TextInputForm(request.POST)
        if form.is_valid():
            text = form.cleaned_data['text']
            sentiment_results = sentiment_model(text, return_all_scores=True)[0]
            label_to_sentiment = {'LABEL_0': 'negative', 'LABEL_1': 'positive'}
            sentiment_scores = {label_to_sentiment[res['label']]: res['score'] for res in sentiment_results}

            rating_results = rating_model(text, return_all_scores=True)[0]
            sorted_ratings = sorted(rating_results, key=lambda x: x['score'], reverse=True)[:3]
            label_to_rating = {0: 1, 1: 2, 2: 3, 3: 4, 4: 7, 5: 8, 6: 9, 7: 10}
            top_ratings = [{"rating": label_to_rating[int(res['label'].split('_')[1])], "score": res['score']} for res in sorted_ratings]

            return render(request, 'classify_text.html', {
                'form': form,
                'sentiment_scores': sentiment_scores,
                'top_ratings': top_ratings
            })
    else:
        form = TextInputForm()

    return render(request, 'classify_text.html', {'form': form})


