import argparse

def read_counter_lines(input_file):
    params_line = None
    counter_lines = []
    packet_count_lines = []
    total_count = None

    lines = open(input_file).readlines()
    for idx, line in enumerate(lines):
        if line.strip() == 'Sketch parameters':
            params_line = lines[idx+1]
        elif line.startswith('total='):
            total_count = int(line.split('=')[1].strip())
        elif line.startswith('Counter:'):
            counter_lines.append(line.split(': ')[1].strip())
        elif line.startswith('Packet count:'):
            packet_count_lines.append(line.split(': ')[1].strip().split(' '))

    return params_line, counter_lines, packet_count_lines, total_count

def parse_params(params_line, packet_count_lines, total_count):
    parsed_params = {}
    tokens = params_line.split(' ')
    tokens = [int(token) for token in tokens]
    
    keys = ['levels', 'rows', 'width', 'heap']
    if len(tokens) == 3:
        # prepend levels=1 to `tokens`
        tokens.insert(0, 1)

    for k,t in zip(keys, tokens):
        parsed_params[k] = t

    if packet_count_lines:
        assert(len(packet_count_lines) == parsed_params['levels'])
        for line in packet_count_lines:
            parsed_params['count_' + str(line[0])] = line[1]

    parsed_params['total_count'] = total_count

    return parsed_params

def parse_counters(counter_lines, parsed_params, dataplane):
    parsed_counters = [0 for i in range(parsed_params['levels'] * parsed_params['rows'] * parsed_params['width'])]
    packet_counts = [0 for i in range(parsed_params['levels'])]

    assert(len(counter_lines) <= len(parsed_counters))

    for idx, line in enumerate(counter_lines):
        tokens = line.split(' ')
        tokens = [int(token) for token in tokens]

        if dataplane == 'dpdk':
            if len(tokens) == 3:
                # non-univmon
                level = 0
            else:
                # univmon
                level = tokens[1]
        
            # based on row-major format
            counter_array_idx = level * parsed_params['width'] * parsed_params['rows'] + tokens[-2] * parsed_params['width'] + tokens[-1]
            parsed_counters[counter_array_idx] = tokens[0]
        elif dataplane == 'xdp':
            if len(tokens) == 2:
                # non-univmon
                level = 0
            else:
                # univmon
                level = tokens[1]

            counter_array_idx = tokens[1]
            parsed_counters[counter_array_idx] = tokens[0]
        else:
            assert(False)

    return parsed_counters

def dump_info(parsed_params, parsed_counters, output_file):
    params_output_file = output_file + '.params'
    counters_output_file_prefix = output_file + '.counters'

    with open(params_output_file, 'w') as fout:
        for k,v in sorted(parsed_params.items(), key=lambda item: item[0]):
            fout.write('{}: {}\n'.format(k, v))

    for i in range(parsed_params['levels']):
        counters_output_file = counters_output_file_prefix + '_' + str(i)

        start_idx = i * parsed_params['rows'] * parsed_params['width']
        end_idx = (i + 1) * parsed_params['rows'] * parsed_params['width']

        with open(counters_output_file, 'w') as fout:
            for line in parsed_counters[start_idx:end_idx]:
                fout.write(str(line) + '\n')

def main(args):
    params_line, counter_lines, packet_count_lines, total_count = read_counter_lines(args.input_file)
    if len(packet_count_lines) == 0:
        packet_count_lines = None
    else:
        pass
        #assert(int(packet_count_lines[0][1]) == total_count)
    parsed_params = parse_params(params_line, packet_count_lines, total_count)
    parsed_counters = parse_counters(counter_lines, parsed_params, args.dataplane)
    dump_info(parsed_params, parsed_counters, args.output_file)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--input_file', required=True)
    parser.add_argument('--output_file', required=True)
    parser.add_argument('--dataplane', required=True)
    args = parser.parse_args()
    main(args)
