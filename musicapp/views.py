from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.core.mail import send_mail
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect
from django.shortcuts import render, reverse
from django.urls import reverse_lazy
from django.views.generic import (
    CreateView,
    DeleteView,
    ListView,
    UpdateView,
    View
)

from .forms import CommentForm, MusicModForm
from .models import CommentMod, ContactMod, MusicMod

# Likes


class LikeCommentView(View):
    """
    Gets likes from comments
    Del dis-like if like
    """
    def post(self, request, pk):
        comment = get_object_or_404(CommentMod, pk=pk)
        user = request.user
        if user.is_authenticated:
            if user not in comment.likes.all():
                comment.likes.add(user)
                comment.dislikes.remove(user)  # remove from dislike
                success_message = ("You have successfully added a like")
                messages.success(self.request, success_message)
                comment.save()
            else:
                success_message = f"You have already liked this comment"
                messages.success(self.request, success_message)

        return HttpResponseRedirect(reverse("song_all_comments"))


# Dislikes


class DisLikeCommentView(View):
    """
    Gets dis-likes from comments
    Del like if dis-like
    """
    def post(self, request, pk):
        comment = get_object_or_404(CommentMod, pk=pk)
        user = request.user
        if user.is_authenticated:
            if user not in comment.dislikes.all():
                comment.dislikes.add(user)
                comment.likes.remove(user)  # remove from likes
                success_message = (
                    f"You have successfully added a Dis-like to this comment"
                )
                messages.success(self.request, success_message)
                comment.save()
            else:
                success_message = f"You have already dis liked this comment"
                messages.success(self.request, success_message)

        return HttpResponseRedirect(reverse("song_all_comments"))


class CommentDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    """
    View for deleting a user's comment.
    allowing only superusers.
    """
    model = CommentMod
    template_name = "musicapp/contact_confirm_delete.html"
    success_url = reverse_lazy("song_all_comments")

    def test_func(self):
        comment = get_object_or_404(CommentMod, pk=self.kwargs["pk"])
        return self.request.user == (
            comment.user_profile.user or self.request.user.is_superuser
            )

    def handle_no_permission(self):
        comment = get_object_or_404(CommentMod, pk=self.kwargs["pk"])
        messages.error(self.request, "You are not the owner of this comment.")
        return redirect("song_all_comments")

    def get_object(self, queryset=None):
        return get_object_or_404(CommentMod, pk=self.kwargs["pk"])

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.delete()
        success_message = f"Comment has been successfully deleted."
        messages.success(self.request, success_message)
        return redirect(self.success_url)


class SongCommentEditView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    """
    Edit view for comments, allowing only the owner access.
    Utilizes LoginRequiredMixin and UserPassesTestMixin.
    """
    model = CommentMod
    template_name = "comments/comment_edit.html"

    def test_func(self):
        comment = get_object_or_404(CommentMod, pk=self.kwargs["pk"])
        return self.request.user == comment.user_profile.user

    def handle_no_permission(self):
        comment = get_object_or_404(CommentMod, pk=self.kwargs["pk"])
        messages.error(self.request, "You are not the owner of this comment.")
        return redirect("song_all_comments")

    def get(self, request, pk):
        comment = get_object_or_404(CommentMod, pk=pk)
        form = CommentForm(instance=comment)
        return render(
            request, (
                "comments/comment_edit.html",
                {"form": form, "comment": comment}
                )
        )

    def post(self, request, pk):
        comment = get_object_or_404(CommentMod, pk=pk)
        form = CommentForm(request.POST, instance=comment)
        if form.is_valid():
            success_message = f"Comment has been successfully edited ."
            messages.success(self.request, success_message)
            form.save()
            return redirect("song_all_comments")
        return render(
            request, "comments/comment_edit.html",
            {"form": form, "comment": comment}
        )


class AddCommentToSongView(CreateView):
    """
    Allow all users to make comments
    """
    model = CommentMod  # Specify the model
    template_name = "comments/comment_add.html"
    form_class = CommentForm

    def form_valid(self, form):
        song = get_object_or_404(MusicMod, pk=self.kwargs["pk"])
        form.instance.music = song
        form.instance.user_profile = self.request.user.userprofile
        return super().form_valid(form)

    def get_success_url(self):
        success_message = f"Comment has been created successfully."
        messages.success(self.request, success_message)
        return reverse("song_all_comments")


class SongListCommentView(ListView):
    """
    View all comments
    """
    model = MusicMod
    template_name = "comments/all_songs_comments.html"
    context_object_name = "songs"

    def get_queryset(self):
        """Order the queryset by song_title."""
        return MusicMod.objects.all().order_by("song_title")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["comments"] = CommentMod.objects.all()
        return context


class SongListView(ListView):
    """
    ListView for displaying a sorted list of songs.
    """

    model = MusicMod
    template_name = "musicapp/song_list.html"
    context_object_name = "songs"

    def get_queryset(self):
        """Order the queryset by song_title."""
        return MusicMod.objects.all().order_by("song_title")


class SongCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    """
    Song creation restricted to superuser
    """
    model = MusicMod
    form_class = MusicModForm
    template_name = "musicapp/song_form.html"
    success_url = reverse_lazy("song_list")

    def test_func(self):
        """
        Check if the current user is a superuser.
        """
        return self.request.user.is_superuser

    def handle_no_permission(self):
        """
        Handle case when the current user is not a superuser.
        Redirects to "song_list" with an error message.
        """
        messages.error(
            self.request, "You do not have permission to add songs."
            )
        return redirect("song_list")

    def form_valid(self, form):
        messages.success(
            self.request,
            f"Successfully added {form.instance.artist_name} - ' \
                {form.instance.song_title} to the database.",
        )
        return super().form_valid(form)


class SongUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    """
    Update view for songs, allowing only superusers.
    """
    model = MusicMod
    form_class = MusicModForm
    template_name = "musicapp/song_update.html"
    success_url = reverse_lazy("song_list")

    def test_func(self):
        """
        Check if the current user is a superuser.
        """
        return self.request.user.is_superuser

    def handle_no_permission(self):
        """
        Handle case when the current user is not a superuser.
        Redirects to "song_list" with an error message.
        """
        messages.error(self.request, "You do not have permission \
            to edit songs.")
        return redirect("song_list")

    def form_valid(self, form):
        messages.success(
            self.request,
            f"Successfully updated {form.instance.artist_name} - ' \
                {form.instance.song_title}.",
        )
        return super().form_valid(form)


class SongDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    """
    Delete view for songs, allowing only superusers.
    """
    model = MusicMod
    template_name = "musicapp/song_confirm_delete.html"

    def test_func(self):
        """
        Check if the current user is a superuser.
        """
        return self.request.user.is_superuser

    def handle_no_permission(self):
        """
        Handle case when the current user is not a superuser.
        Redirects to "song_list" with an error message.
        """
        messages.error(self.request, (
            "You do not have permission to delete songs."))
        return redirect("song_list")

    def get_success_url(self):
        return reverse_lazy("song_list")

    def delete(self, request, *args, **kwargs):
        if not self.request.user.is_superuser:
            messages.error(self.request, (
                "Sorry, only administrators can delete songs."))
            return self.handle_no_permission()

        messages.success(
            self.request,
            f"Successfully deleted {self.get_object().artist_name} - ' \
                {self.get_object().song_title}.",
        )
        return super().delete(request, *args, **kwargs)


class ContactUsView(CreateView):
    """
    Contacts page view
    """
    template_name = "comments/contact_us.html"
    model = ContactMod
    fields = [
        "fname",
        "lname",
        "email",
        "phone",
        "msg",
    ]  # List all the fields in your form
    success_url = reverse_lazy("contact_us")

    def form_valid(self, form):
        # Save the form data to the database
        response = super().form_valid(form)

        # Send verification email to the user
        self.send_verification_email()

        # Send email notification
        self.send_notification_email()

        # Display success message
        messages.success(
            self.request, (
                "Your message was sent successfully. We will be in touch .",
                )
        )

        return response

    def form_invalid(self, form):
        # Handle form validation errors
        messages.error(
            self.request,
            "There was an error with your entry. Please check your input.",
        )
        return super().form_invalid(form)

    def send_verification_email(self):
        instance = self.object

        # Send email to the user for verification
        user_subject = "Contact Form Submission Verification"
        user_message = (
            f"Thank you for contacting us! Your message \
            has been received.\n\nMessage: {instance.msg}")
        user_from_email = "bluepulseband@gmail.com"
        user_recipient_list = [instance.email]
        print(f"User Recipient List: {user_recipient_list}")

        send_mail(
            user_subject, user_message, user_from_email, user_recipient_list)

    def send_notification_email(self):
        instance = self.object

        # Send email notification to admin 'bluepulseband@gmail.com'
        admin_subject = "New Contact Form Submission"
        admin_message = (f"A new contact form submission:\n\nName: ' \
        {instance.fname} {instance.lname}\nEmail: {instance.email}\nPhone: ' \
            {instance.phone}\nMessage: {instance.msg}")
        admin_from_email = "bluepulseband@gmail.com"
        admin_recipient_list = ["bluepulseband@gmail.com"]

        send_mail(
            admin_subject,
            admin_message,
            admin_from_email,
            admin_recipient_list
            )

        return reverse("contact_us")


#############
def handler404(request, exception):
    """
    This is a 404 page to catch errors
    """
    return render(request, "404.html", status=404)
