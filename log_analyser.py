import re
import json
import subcommand


TASK_ID_REG = re.compile('[0-9]{19}')


def pick_task_info(content, task_store):
    log = json.loads(content)
    msg = log['msg']
    key = TASK_ID_REG.findall(msg)

    if key:
        task_store.setdefault(key[0], []).append(msg)


def main():

    task_store = {}

    with file("scheduler.log", "r") as f:
        for log in f:
            pick_task_info(log, task_store)

    with file("analysis_result.json", 'w') as output:
        output.write(json.dumps(task_store))


@subcommand.subcommand()
def query_logs(options):
    """Display task id logs.

    Usage: hello [options] [name]

    Options:

    -p [--prefix] prefix    : message prefix (default: None)
    """
    result_list = []
    with file("analysis_result.json", "r") as f:
        data = json.load(f)

    try:
        result_list = data[options.prefix]
    except:
        print "No Found!"

    result_iter = iter(result_list)
    print "Task ID:" + options.prefix
    print "Logs   :"
    for i in result_iter:
        print i
        result_iter.next


if __name__ == "__main__":
    main()
    subcommand.main()
