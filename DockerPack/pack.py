import os
import docker
import argparse

client = docker.from_env()


def create_dockerfile(local_dir_name, git_url, work_dir_name, run_cmd):
    __dockerfile = ['FROM python:3.6 \n']
    if git_url is not None:
        __dockerfile.append('RUN git clone {} \n'.format(git_url))
    else:
        __dockerfile.append('COPY {} {} \n'.format(local_dir_name, work_dir_name))
    __dockerfile.extend([
        'WORKDIR {} \n'.format(work_dir_name),
        'RUN pip install -r ./requirements.txt \n'.format(work_dir_name),
        'CMD {}~'.format(str(run_cmd.split(",")))])
    with open("Dockerfile", 'w') as f:
        for cmd in __dockerfile:
            f.write(cmd)


def build(tag):
    """
    for line in client.build(path='.', tag=tag):
        log = line.decode('utf-8').split('\r\n')
        for item in log:
            if item.find("stream") > -1:
                print((json.loads(item))['stream'])
    """
    os.system("docker build -t {} .".format(tag))


def push(tag, repo):
    image_id = get_image_id(tag=tag)
    os.system("docker tag {} {}".format(image_id, repo))
    os.system("docker push {}".format(repo))
    # client.push(repository=repo)


def get_image_id(tag):
    for item in client.images():
        if tag in item["RepoTags"]:
            return (item["Id"].replace("sha256:", ""))[:12]


def main():
    parse = argparse.ArgumentParser()

    parse.add_argument("-l", "--local")
    parse.add_argument("-g", "--git", default=None)
    parse.add_argument("-w", "--work")
    parse.add_argument("-t", "--tag")
    parse.add_argument("-c", "--command")

    parse.add_argument("-r", "--repo", default=None)

    args = parse.parse_args()

    create_dockerfile(local_dir_name=args.local, git_url=args.git, work_dir_name=args.work, run_cmd=str(args.command))
    build(tag=args.tag)
    if args.repo:
        push(tag=args.tag, repo=args.repo)
    client.close()


def test():
    pass


if __name__ == "__main__":
    main()
