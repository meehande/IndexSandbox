import os


def safely_create_output_dir(output_path):
    output_dir = os.path.dirname(output_path)
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)


def write_file(data, output_path):
    safely_create_output_dir(output_path)
    with open(output_path, 'wb') as f:
        f.write(data)
