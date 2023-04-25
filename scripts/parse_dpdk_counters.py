import argparse

def read_counter_lines(input_file):
    params_line = None
    counter_lines = []

    lines = open(input_file).readlines()
    for idx, line in enumerate(lines):
        if line.strip() == 'Sketch parameters':
            params_line = lines[idx+1]
        elif line.strip() == 'Finished printing counters':
            break
        elif line.startswith('Counter:'):
            counter_lines.append(line.split(': ')[1].strip())

    return params_line, counter_lines

def parse_params(params_line):
    parsed_params = {}
    tokens = params_line.split(' ')
    tokens = [int(token) for token in tokens]
    
    keys = ['rows', 'width', 'heap']
    if len(tokens) == 4:
        keys.insert('levels', 0)

    for k,t in zip(keys, tokens):
        parsed_params[k] = t

    return parsed_params

def parse_counters(counter_lines, parsed_params):
    parsed_counters = [0 for i in range(parsed_params['rows'] * parsed_params['width'])]

    for idx, line in enumerate(counter_lines):
        tokens = line.split(' ')
        tokens = [int(token) for token in tokens]

        # based on row-major format
        counter_array_idx = tokens[1] * parsed_params['width'] + tokens[2]
        parsed_counters[counter_array_idx] = tokens[0]

    return parsed_counters

def dump_info(parsed_params, parsed_counters, output_file):
    params_output_file = output_file + '.params'
    counters_output_file = output_file + '.counters'

    with open(params_output_file, 'w') as fout:
        for k,v in parsed_params.items():
            fout.write('{}: {}\n'.format(k, v))

    with open(counters_output_file, 'w') as fout:
        for line in parsed_counters:
            fout.write(str(line) + '\n')

def main(args):
    params_line, counter_lines = read_counter_lines(args.input_file)
    parsed_params = parse_params(params_line)
    parsed_counters = parse_counters(counter_lines, parsed_params)
    dump_info(parsed_params, parsed_counters, args.output_file)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--input_file', required=True)
    parser.add_argument('--output_file', required=True)
    args = parser.parse_args()
    main(args)
