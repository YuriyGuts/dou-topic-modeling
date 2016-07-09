#!/usr/bin/env python3

import codecs
import glob
import os
import re
import sys


def clean_comment(comment):
    clean = comment

    # Convert to lowercase.
    clean = clean.lower()

    # It would be better to precompile all regexes, but even this version is fast enough.
    re_flags = re.MULTILINE | re.UNICODE

    # Remove URLs.
    clean = re.sub(r'''(?i)\b((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:'".,<>?]))''', u"url", clean, flags=re_flags)

    # Remove emails.
    clean = re.sub(r'[\w\.-]+@[\w\.-]+', u"email", clean, flags=re_flags)

    # Convert fancy symbols to ASCII equivalents.
    clean = re.sub(r'\xab|\xbb|\u201c|\u201d|\u201e|\u2033', u'"', clean, flags=re_flags) 
    clean = re.sub(r'\u2018|\u2019|\u201a|\u2032', u"'", clean, flags=re_flags)
    clean = re.sub(r'\u2011|\u2013|\u2014', u"-", clean, flags=re_flags)
    clean = re.sub(r'\u2022', u"*", clean, flags=re_flags)
    clean = re.sub(r'\u2260', u"!=", clean, flags=re_flags)
    clean = re.sub(r'\u0020|\u00a0|\u1680|\u180e|\u2000|\u2001|\u2002|\u2003|\u2004|\u2005|\u2006|\u2007|\u2008|\u2009|\u200a|\u200b|\u202f|\u205f|\u3000|\ufeff', u" ", clean, flags=re_flags)

    # Drop unnecessary symbols to save memory.
    clean = re.sub(r'[\u05d0-\U0001f638]*', u"", clean, flags=re_flags)
    clean = re.sub(r'[\u0100-\u03ff]*', u"", clean, flags=re_flags)
    clean = re.sub(r'[\xa0-\xff]*', u"", clean, flags=re_flags)

    # Squash multiple spaces and line endings into one.
    clean = re.sub(r'\s+', u" ", clean, flags=re_flags)
    clean = re.sub(r'\n+', u"\n", clean, flags=re_flags)

    # Remove surrogate pairs.
    clean = re.sub(r'[^\u0000-\uD7FF\uE000-\uFFFF]', u"", clean, flags=re_flags)

    return clean


def main():
    raw_folder = os.path.join("data", "raw")
    clean_folder = os.path.join("data", "clean")

    if not os.path.exists(clean_folder):
        os.makedirs(clean_folder)

    for comment_file in glob.glob(os.path.join(raw_folder, "comments-*.txt")):
        with codecs.open(comment_file, "r", "utf-8", errors="replace") as comments_file:
            separator = "\n" + "-" * 50 + "\n"
            comments = comments_file.read().split(separator)

            # Clean up every comment.
            clean_comments = [
                clean_comment(comment)
                for comment in comments
            ]

            # Remove comments that are too short: might be not informative enough.
            clean_comments = [
                comment
                for comment in clean_comments
                if len(comment) > 15
            ]

            clean_text = "\n".join(clean_comments)

        # Write the clean version of this comment file.
        clean_file = os.path.basename(comment_file).replace("comments-", "clean-comments-")
        with codecs.open(os.path.join(clean_folder, clean_file), "w", "utf-8") as output:
            output.write(clean_text)


if __name__ == "__main__":
    main()
