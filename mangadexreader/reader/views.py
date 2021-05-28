from django.shortcuts import render

from .forms import AdvancedSearch
from .utils import new_session
from . import wrapper


# Create your views here.
def index(request):
    form = AdvancedSearch()
    return render(request, 'reader/index.html', {'form': form})


def manga_list(request, manga_list=None):
    if request.method == 'POST':
        form = AdvancedSearch(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            print(data)
            params = {
                'title': data['title'] if data['title'] != '' else None,
                # 'authors[]': [author.strip() for author in data['authors'].split(',')],
                # 'artists[]': [artist.strip() for artist in data['artists'].split(',')],
                'year': data['year'],
                'includedTags[]': data['includedTags']
            }
            manga_list = wrapper.get_manga_list(params)
            print(manga_list)
            return render(request, 'reader/manga_list.html',{
                'manga_list': manga_list
            })
    return render(request, 'reader/manga_list.html', {
        'manga_list': manga_list
    })


def manga(request, manga_id, offset=0):
    manga = wrapper.get_manga(manga_id)
    limit = 10
    chapter_list = wrapper.get_manga_chapters(manga_id, offset=offset)
    return render(request, 'reader/manga.html', {
        'manga_id': manga_id,
        'manga': manga,
        'chapters': chapter_list['chapters'],
        'prev': offset - limit if offset - limit > 0 else 0,
        'next': offset + limit if offset + limit < chapter_list['total'] else None
    })


def chapter(request, chapter_id, page):
    if len(request.session.keys()) == 0:
        request.session = new_session()
    if chapter_id != request.session['chapter']['id']:
        server_base_url = wrapper.get_mangadexahome_server_url(chapter_id)
        details = wrapper.get_chapter(chapter_id)
        request.session["chapter"] = {
            'id': chapter_id,
            'serverBaseURL': server_base_url,
            'hash': details["hash"],
            'data': details["data"],
            'dataSaver': details["dataSaver"],
        }
        if request.session['manga']['id'] != details['mangaID']:
            manga_details = wrapper.get_manga(details['mangaID'])
            request.session['manga'] = {
                'id': details['mangaID'],
                'title': manga_details['title']
            }
    src = f"{server_base_url}/data/{request.session['chapter']['hash']}/{request.session['chapter']['data'][page]}"
    return render(request, 'reader/page.html', {
        'manga_id': request.session['manga']['id'],
        'manga_title': request.session['manga']['title'],
        'src': src,
        'chapter_id': chapter_id,
        'prev': page - 1 if page > 0 else None,
        'next': page + 1 if page < len(details["data"]) else None
    })

