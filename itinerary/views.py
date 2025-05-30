from django.shortcuts import render, get_object_or_404
from datetime import timedelta
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
import json
from datetime import datetime
from django.db import models
from .models import Itineraries, PlaceCards


def safe_strip(value):
    """Safely strip a value that might be None"""
    if value is None:
        return ''
    return str(value).strip()


def safe_float(value):
    """Safely convert a value to float, return None if not possible"""
    if not value or value == '':
        return None
    try:
        return float(value)
    except (ValueError, TypeError):
        return None


@login_required
@csrf_exempt
def create_itinerary(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            
            # Get data from request
            trip_title = data.get('trip_title', 'Untitled Trip')
            start_date = data.get('start_date')
            return_date = data.get('return_date')
            
            # Create the itinerary
            itinerary = Itineraries.objects.create(
                user=request.user,
                title=trip_title,
                start_date=start_date,
                return_date=return_date,
            )
            
            return JsonResponse({
                'success': True,
                'itinerary_id': itinerary.id,
                'message': 'Itinerary created successfully!'
            })
            
        except Exception as e:
            return JsonResponse({
                'success': False,
                'message': f'Error creating itinerary: {str(e)}'
            })
    
    return JsonResponse({
        'success': False,
        'message': 'Invalid request method'
    })


@login_required
def edit_itinerary(request, itinerary_id):
    itinerary = get_object_or_404(Itineraries, id=itinerary_id, user=request.user)
    start = itinerary.start_date
    duration = itinerary.duration
    date_list = [start + timedelta(days=i) for i in range(duration)]
    
    # Load existing place cards
    place_cards = PlaceCards.objects.filter(itinerary=itinerary).order_by('date', 'order', 'start_time')
    
    return render(request, 'itinerary/edit_itinerary.html', {
        "itinerary": itinerary,
        "date_list": date_list,
        "place_cards": place_cards,
    })


@login_required
@csrf_exempt
def save_place_card(request, itinerary_id):
    """Create or update a place card"""
    if request.method != 'POST':
        return JsonResponse({'success': False, 'message': 'Invalid request method'})
    
    try:
        # Verify itinerary belongs to user
        itinerary = get_object_or_404(Itineraries, id=itinerary_id, user=request.user)
        
        data = json.loads(request.body)
        print(f"Received data: {data}")  # Debug log
        
        card_id = data.get('card_id')  # If editing existing card
        
        # Parse date
        date_str = data.get('date')
        if not date_str:
            return JsonResponse({'success': False, 'message': 'Date is required'})
            
        try:
            date = datetime.strptime(date_str, '%Y-%m-%d').date()
        except ValueError:
            return JsonResponse({'success': False, 'message': 'Invalid date format'})
        
        # Parse times
        start_time = None
        end_time = None
        if data.get('start_time'):
            try:
                start_time = datetime.strptime(data.get('start_time'), '%H:%M').time()
            except ValueError:
                return JsonResponse({'success': False, 'message': 'Invalid start time format'})
        if data.get('end_time'):
            try:
                end_time = datetime.strptime(data.get('end_time'), '%H:%M').time()
            except ValueError:
                return JsonResponse({'success': False, 'message': 'Invalid end time format'})
        
        # Calculate order for new cards
        if not card_id:
            # For new cards, find the highest order for this date and add 1
            max_order = PlaceCards.objects.filter(
                itinerary=itinerary, 
                date=date
            ).aggregate(models.Max('order'))['order__max']
            order = (max_order or -1) + 1
            print(f"New card order calculated: {order}")  # Debug log
        else:
            # For existing cards, keep the current order or use provided order
            try:
                existing_card = PlaceCards.objects.get(id=card_id, itinerary=itinerary)
                order = data.get('order', existing_card.order)
                print(f"Existing card order: {order}")  # Debug log
            except PlaceCards.DoesNotExist:
                return JsonResponse({'success': False, 'message': 'Card not found'})

        # Prepare place card data with proper null handling using helper functions
        place_data = {
            'title': safe_strip(data.get('title')),
            'date': date,
            'start_time': start_time,
            'end_time': end_time,
            'notes': safe_strip(data.get('notes')),
            'google_place_id': safe_strip(data.get('place_id')),
            'google_place_name': safe_strip(data.get('original_place_name')),
            'latitude': safe_float(data.get('place_lat')),
            'longitude': safe_float(data.get('place_lng')),
            'address': safe_strip(data.get('place_address')),
            'order': order,
        }
        
        if not place_data['title']:
            return JsonResponse({'success': False, 'message': 'Title is required'})
        
        print(f"Place data to save: {place_data}")  # Debug log
        
        if card_id:
            # Update existing card
            place_card = get_object_or_404(PlaceCards, id=card_id, itinerary=itinerary)
            for key, value in place_data.items():
                setattr(place_card, key, value)
            place_card.save()
            action = 'updated'
            print(f"Updated card ID: {place_card.id}")  # Debug log
        else:
            # Create new card
            place_card = PlaceCards.objects.create(
                itinerary=itinerary,
                **place_data
            )
            action = 'created'
            print(f"Created new card ID: {place_card.id}")  # Debug log
        
        return JsonResponse({
            'success': True,
            'card_id': place_card.id,
            'message': f'Place card {action} successfully!',
            'action': action
        })
        
    except json.JSONDecodeError:
        return JsonResponse({'success': False, 'message': 'Invalid JSON data'})
    except Exception as e:
        print(f"Error saving place card: {str(e)}")  # Debug log
        return JsonResponse({
            'success': False,
            'message': f'Error saving place card: {str(e)}'
        })


@login_required
@csrf_exempt
def delete_place_card(request, itinerary_id, card_id):
    """Delete a place card"""
    if request.method != 'DELETE':
        return JsonResponse({'success': False, 'message': 'Invalid request method'})
    
    try:
        # Verify itinerary belongs to user
        itinerary = get_object_or_404(Itineraries, id=itinerary_id, user=request.user)
        place_card = get_object_or_404(PlaceCards, id=card_id, itinerary=itinerary)
        
        place_card.delete()
        
        return JsonResponse({
            'success': True,
            'message': 'Place card deleted successfully!'
        })
        
    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': f'Error deleting place card: {str(e)}'
        })


@login_required
@csrf_exempt
def update_card_order(request, itinerary_id):
    """Update the order of place cards after drag and drop"""
    if request.method != 'POST':
        return JsonResponse({'success': False, 'message': 'Invalid request method'})
    
    try:
        # Verify itinerary belongs to user
        itinerary = get_object_or_404(Itineraries, id=itinerary_id, user=request.user)
        
        data = json.loads(request.body)
        card_orders = data.get('card_orders', [])  # List of {card_id, date, order}
        
        # Update each card's order and date
        for card_data in card_orders:
            card_id = card_data.get('card_id')
            new_date = datetime.strptime(card_data.get('date'), '%Y-%m-%d').date()
            new_order = card_data.get('order', 0)
            
            place_card = get_object_or_404(PlaceCards, id=card_id, itinerary=itinerary)
            place_card.date = new_date
            place_card.order = new_order
            place_card.save()
        
        return JsonResponse({
            'success': True,
            'message': 'Card order updated successfully!'
        })
        
    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': f'Error updating card order: {str(e)}'
        })
    

@login_required
def save_itinerary(request, itinerary_id):
    itinerary = get_object_or_404(Itineraries, id=itinerary_id, user=request.user)
    start = itinerary.start_date
    duration = itinerary.duration
    date_list = [start + timedelta(days=i) for i in range(duration)]
    
    # Load existing place cards
    place_cards = PlaceCards.objects.filter(itinerary=itinerary).order_by('date', 'order', 'start_time')
    
    return render(request, 'itinerary/save_itinerary.html', {
        "itinerary": itinerary,
        "date_list": date_list,
        "place_cards": place_cards,
    })

# Add this to your views.py

@login_required
@csrf_exempt
def update_itinerary(request, itinerary_id):
    """Update itinerary details including title, dates, and description"""
    if request.method != 'POST':
        return JsonResponse({'success': False, 'message': 'Invalid request method'})
    
    try:
        # Verify itinerary belongs to user
        itinerary = get_object_or_404(Itineraries, id=itinerary_id, user=request.user)
        
        data = json.loads(request.body)
        print(f"Received itinerary update data: {data}")  # Debug log
        
        # Get updated fields
        title = safe_strip(data.get('title'))
        start_date_str = data.get('start_date')
        return_date_str = data.get('return_date')
        description = safe_strip(data.get('description'))
        delete_conflicting_cards = data.get('delete_conflicting_cards', False)
        
        # Validate required fields
        if not title:
            return JsonResponse({'success': False, 'message': 'Title is required'})
        
        if not start_date_str or not return_date_str:
            return JsonResponse({'success': False, 'message': 'Start and return dates are required'})
        
        # Parse dates
        try:
            start_date = datetime.strptime(start_date_str, '%Y-%m-%d').date()
            return_date = datetime.strptime(return_date_str, '%Y-%m-%d').date()
        except ValueError:
            return JsonResponse({'success': False, 'message': 'Invalid date format'})
        
        # Validate date logic
        if return_date <= start_date:
            return JsonResponse({'success': False, 'message': 'Return date must be after start date'})
        
        # Check trip duration (max 30 days)
        duration = (return_date - start_date).days + 1
        if duration > 30:
            return JsonResponse({'success': False, 'message': 'Trip duration cannot exceed 30 days'})
        
        # Store original dates for comparison
        original_start = itinerary.start_date
        original_return = itinerary.return_date
        
        # Check for conflicting place cards if dates changed
        conflicting_cards = []
        deleted_count = 0
        
        if start_date != original_start or return_date != original_return:
            conflicting_cards = PlaceCards.objects.filter(
                itinerary=itinerary
            ).filter(
                models.Q(date__lt=start_date) | models.Q(date__gt=return_date)
            )
            
            # Always delete conflicting cards when dates change
            if conflicting_cards.exists():
                deleted_count = conflicting_cards.count()
                print(f"Deleting {deleted_count} conflicting place cards")
                conflicting_cards.delete()
        
        # Begin transaction to ensure data consistency
        from django.db import transaction
        
        with transaction.atomic():
            # Update itinerary
            itinerary.title = title
            itinerary.start_date = start_date
            itinerary.return_date = return_date
            itinerary.description = description or ''
            itinerary.save()
            
            print(f"Updated itinerary {itinerary_id}: {title} ({start_date} to {return_date})")
        
        return JsonResponse({
            'success': True,
            'message': 'Itinerary updated successfully!',
            'itinerary': {
                'id': itinerary.id,
                'title': itinerary.title,
                'start_date': itinerary.start_date.strftime('%Y-%m-%d'),
                'return_date': itinerary.return_date.strftime('%Y-%m-%d'),
                'description': itinerary.description or '',
                'duration': itinerary.duration
            },
            'deleted_cards': deleted_count
        })
        
    except json.JSONDecodeError:
        return JsonResponse({'success': False, 'message': 'Invalid JSON data'})
    except Exception as e:
        print(f"Error updating itinerary: {str(e)}")  # Debug log
        import traceback
        traceback.print_exc()  # Print full traceback for debugging
        return JsonResponse({
            'success': False,
            'message': f'Error updating itinerary: {str(e)}'
        })


# Add this URL pattern to your urls.py
# path('itinerary/<int:itinerary_id>/update/', views.update_itinerary, name='update_itinerary'),