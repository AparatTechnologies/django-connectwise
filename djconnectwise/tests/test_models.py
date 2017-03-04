from djconnectwise.models import TicketPriority, BoardStatus

from model_mommy import mommy
from test_plus.test import TestCase
from djconnectwise.models import Ticket, InvalidStatusError
from unittest.mock import patch


class ModelTestCase(TestCase):

    def setUp(self):
        self.members = mommy.make_recipe(
            'djconnectwise.tests.member',
            _quantity=3
        )
        self.projects = mommy.make_recipe(
            'djconnectwise.tests.project',
            _quantity=4,
        )
        self.companies = mommy.make_recipe(
            'djconnectwise.tests.company',
            _quantity=2
        )
        self.ticket_priorities = mommy.make_recipe(
            'djconnectwise.tests.ticket_priority',
            _quantity=3
        )
        self.connectwise_boards = mommy.make_recipe(
            'djconnectwise.tests.connectwise_board',
            _quantity=3,
        )
        self.board_statuses = mommy.make_recipe(
            'djconnectwise.tests.ticket_status',
            _quantity=7,
        )
        # TODO: remove prints
        print()
        for s in BoardStatus.objects.all():
            print(s.board.name, s.name, s.closed_status)
        BoardStatus.objects.filter(
            name__in=['Completed', 'Closed']
        ).update(closed_status=True)
        for s in BoardStatus.objects.all():
            print(s.board, s.name, s.closed_status)
        # All the statuses belong to the first board.
        for status in self.board_statuses:
            status.board = self.connectwise_boards[0]
            status.save()
        for s in BoardStatus.objects.all():
            print(s.board.name, s.name, s.closed_status)
        print()


class TestTicketPriority(TestCase):

    def test_priority_color(self):
        # If a priority has a color, then the property returns it.
        p = TicketPriority(name='Priority 1 - Emergency Response')
        # This also tests the setter.
        p.color = 'PapayaWhip'  # Yeah, PapayaWhip is a CSS color
        self.assertEqual(p.color, 'PapayaWhip')

    def test_priority_color_property(self):
        # If a priority doesn't have a color, then the property returns
        # a sensible default.
        p = TicketPriority(name='Priority 1 - Emergency Response')
        self.assertEqual(p.color, 'red')
        p = TicketPriority(name='Priority 2 - Quick Response')
        self.assertEqual(p.color, 'orange')
        p = TicketPriority(name='Priority 3 - Normal Response')
        self.assertEqual(p.color, 'yellow')
        p = TicketPriority(name='Priority 4 - Scheduled Maintenance')
        self.assertEqual(p.color, 'white')
        p = TicketPriority(name='Priority 5 - Next Time')
        self.assertEqual(p.color, 'darkmagenta')
        p = TicketPriority(name='Totally unknown priority')
        self.assertEqual(p.color, 'darkgray')


class TestBoard(ModelTestCase):
    def test_get_closed_status_prefers_closed(self):
        board = self.connectwise_boards[0]
        closed_status = board.get_closed_status()
        print()
        print(closed_status.closed_status)
        print()
        self.assertEqual(
            board.get_closed_status().name,
            'Closed'
        )

    def test_get_closed_status_any_closed(self):
        # Return some closed status if there's not a closed status called
        # 'Closed'
        board = self.connectwise_boards[0]
        board.board_statuses.filter(name='Closed').delete()
        closed_status = board.get_closed_status()
        self.assertTrue(closed_status.closed_status)
        self.assertNotEqual(
            closed_status.name,
            'Closed'
        )

    def test_get_closed_status_no_closed(self):
        # Return None if there's no closed statuses
        board = self.connectwise_boards[0]
        board.board_statuses.filter(closed_status=True).delete()
        closed_status = board.get_closed_status()
        self.assertEqual(closed_status, None)


class TestTicket(ModelTestCase):

    def test_str(self):
        t = Ticket(id=1, summary='Únicôde wôrks!')
        self.assertEqual(
            '{}'.format(t),
            '1-Únicôde wôrks!'
        )

    def test_save_checks_status(self):
        # Raises an exception if the ticket status isn't valid for the
        # ticket's board.
        ticket = Ticket.objects.create(
            summary='test',
            status=self.connectwise_boards[0].board_statuses.first(),
            board=self.connectwise_boards[0]
        )
        ticket.save()  # Should work
        with self.assertRaises(InvalidStatusError):
            ticket.board = self.connectwise_boards[1]
            ticket.save()

    def test_save_calls_update_cw(self):
        # TODO
        self.assertTrue(False)

    def test_update_cw(self):
        # Verify update_cw calls the API client
        # TODO
        self.assertTrue(False)

    def test_close_ticket(self):
        # Verify close calls save.
        # TODO
        board = self.connectwise_boards[0]
        ticket = Ticket.objects.create(
            summary='test',
            status=board.board_statuses.first(),
            board=board
        )
        with patch.object(ticket, 'save') as mock_save:
           ticket.close()
           print(mock_save)
           mock_save.assert_called_once()

    def test_close_ticket_no_closed_statuses(self):
        # Raises an exception if there are no available closed statuses for
        # the ticket's board.
        board = self.connectwise_boards[0]
        board.board_statuses.filter(closed_status=True).delete()

        ticket = Ticket.objects.create(
            summary='test',
            status=board.board_statuses.first(),
            board=board
        )
        ticket.save()  # Should work
        with self.assertRaises(InvalidStatusError):
            ticket.close()
