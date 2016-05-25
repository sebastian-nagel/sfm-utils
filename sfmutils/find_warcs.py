#!/usr/bin/env python

from sfmutils.api_client import ApiClient
import argparse
import logging
import sys

log = logging.getLogger(__name__)


def main(sys_argv):
    # Arguments
    parser = argparse.ArgumentParser(description="Return WARC filepaths for passing to other commandlines.")
    parser.add_argument("--include-web", action="store_true", help="Include WARCs for web harvests.")
    parser.add_argument("--harvest-start", help="ISO8601 datetime after which harvest was performed. For example, "
                                                "2015-02-22T14:49:07Z")
    parser.add_argument("--harvest-end", help="ISO8601 datetime before which harvest was performed. For example, "
                                              "2015-02-22T14:49:07Z")
    default_api_base_url = "http://api"
    parser.add_argument("--api-base-url", help="Base url of the SFM API. Default is {}.".format(default_api_base_url),
                        default=default_api_base_url)
    parser.add_argument("--debug", type=lambda v: v.lower() in ("yes", "true", "t", "1"), nargs="?",
                        default="False", const="True")
    parser.add_argument("seedset", nargs="+", help="Limit to WARCs of this seedset. "
                                                   "Truncated seedset ids may be used.")

    # Explicitly using sys.argv so that can mock out for testing.
    args = parser.parse_args(sys_argv[1:])

    # Logging
    logging.basicConfig(format='%(asctime)s: %(name)s --> %(message)s',
                        level=logging.DEBUG if args.debug else logging.INFO)
    logging.getLogger("requests").setLevel(logging.DEBUG if args.debug else logging.INFO)

    api_client = ApiClient(args.api_base_url)
    seedset_ids = []
    for seedset_id_part in args.seedset:
        log.debug("Looking up seedset id part %s", seedset_id_part)
        if len(seedset_id_part) == 32:
            seedset_ids.append(seedset_id_part)
        else:
            seedsets = list(api_client.seedsets(seedset_id_startswith=seedset_id_part))
            if len(seedsets) == 0:
                print "No matching seedsets for {}".format(seedset_id_part)
                sys.exit(1)
                return
            elif len(seedsets) > 1:
                print "Multuple matching seedsets for {}".format(seedset_id_part)
                sys.exit(1)
                return
            else:
                seedset_ids.append(seedsets[0]["seedset_id"])
    warc_filepaths = set()
    for seedset_id in seedset_ids:
        log.debug("Looking up warcs for %s", seedset_id)
        warcs = api_client.warcs(seedset_id=seedset_id, harvest_date_start=args.harvest_start,
                                 harvest_date_end=args.harvest_end, exclude_web=not args.include_web)
        for warc in warcs:
            warc_filepaths.add(warc["path"])
    return " ".join(sorted(warc_filepaths))

if __name__ == "__main__":
    print main(sys.argv)