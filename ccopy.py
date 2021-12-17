#!/usr/bin/env python3

import praw
import sys
import time

USER_AGENT = "Romania moderator bot by /u/programatorulupeste"

# Check that all the args are provided
if len(sys.argv) != 5:
    print("Argument error.")
    print("\tUsage: %s source_url destination_url user password" % sys.argv[0])
    exit(1)

# Create the reddit instance
reddit = praw.Reddit(
        "ro_moderator_bot",
        user_agent=USER_AGENT,
        username=sys.argv[3],
        password=sys.argv[4])

# Create source and destination submissions
source = praw.models.Submission(reddit, url=sys.argv[1])
destination = praw.models.Submission(reddit, url=sys.argv[2])

# Get the comments by new and get the reversed list
source.comment_sort = "new"
src_comments = reversed(source.comments.list())


for comm in src_comments:
    if isinstance(comm, praw.models.MoreComments):
        continue

    # For each parent comment, post in the destination thread
    if comm.is_root and comm.author:
        reply_body = "Intrebare de la /u/%s:\n***\n%s" \
            % (comm.author, str(comm.body))

        print("Posting " + str(reply_body))
        destination.reply(reply_body)

        print("Waiting 5s")
        time.sleep(5)

print("\nDone!")
