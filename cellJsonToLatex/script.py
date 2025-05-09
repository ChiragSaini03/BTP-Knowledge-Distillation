import json
import sys
import statistics


def cluster_positions(positions):
    """
    Cluster a sorted list of positions into groups separated by large gaps.
    Uses median of adjacent gaps to determine threshold.
    Returns list of cluster centers.
    """
    if len(positions) < 2:
        return positions[:]
    # compute adjacent differences
    diffs = [positions[i+1] - positions[i] for i in range(len(positions)-1)]
    # median gap
    median_diff = statistics.median(diffs)
    # use half median_gap as threshold
    threshold = median_diff / 2.0
    clusters = []
    current = [positions[0]]
    for pos, diff in zip(positions[1:], diffs):
        if diff <= threshold:
            current.append(pos)
        else:
            clusters.append(sum(current) / len(current))
            current = [pos]
    clusters.append(sum(current) / len(current))
    return clusters


def generate_grid(cells):
    # compute centers
    for c in cells:
        c['x_center'] = c['x'] + c['width']/2.0
        c['y_center'] = c['y'] + c['height']/2.0
    # sort positions
    x_positions = sorted(c['x_center'] for c in cells)
    y_positions = sorted(c['y_center'] for c in cells)
    col_centers = sorted(cluster_positions(x_positions))
    row_centers = sorted(cluster_positions(y_positions))
    # assign indices
    for c in cells:
        c['col'] = min(range(len(col_centers)), key=lambda i: abs(c['x_center'] - col_centers[i]))
        c['row'] = min(range(len(row_centers)), key=lambda i: abs(c['y_center'] - row_centers[i]))
    # compute spans
    occupied = set()
    R, C = len(row_centers), len(col_centers)
    grid = [[None]*C for _ in range(R)]
    for c in sorted(cells, key=lambda c: (c['row'], c['col'])):
        r, col = c['row'], c['col']
        if (r, col) in occupied:
            continue
        # colspan: count consecutive columns inside bounding box
        cs = 0
        for j in range(col, C):
            # column center inside cell horizontally?
            if c['x'] <= col_centers[j] <= c['x']+c['width']:
                cs += 1
            else:
                break
        # rowspan similarly
        rs = 0
        for i in range(r, R):
            if c['y'] <= row_centers[i] <= c['y']+c['height']:
                rs += 1
            else:
                break
        c['colspan'] = cs
        c['rowspan'] = rs
        grid[r][col] = c
        # mark occupied
        for dr in range(rs):
            for dc in range(cs):
                occupied.add((r+dr, col+dc))
    return grid


def latex_from_grid(grid):
    if not grid:
        return ''
    R, C = len(grid), len(grid[0])
    lines = ['% Auto-generated LaTeX table', f'\\begin{{tabular}}{{{"c"*C}}}', '\\toprule']
    for i, row in enumerate(grid):
        elems = []
        j = 0
        while j < C:
            cell = row[j]
            if cell is None:
                elems.append('')
                j += 1
                continue
            content = cell.get('text','')
            rs, cs = cell['rowspan'], cell['colspan']
            if rs>1 and cs>1:
                elem = f"\\multirow{{{rs}}}{{*}}{{\\multicolumn{{{cs}}}{{c}}{{{content}}}}}"
            elif cs>1:
                elem = f"\\multicolumn{{{cs}}}{{c}}{{{content}}}"
            elif rs>1:
                elem = f"\\multirow{{{rs}}}{{*}}{{{content}}}"
            else:
                elem = content
            elems.append(elem)
            j += cs
        lines.append(' & '.join(elems) + ' \\\\')
        if i==0:
            lines.append('\\midrule')
    lines.append('\\bottomrule')
    lines.append('\\end{tabular}')
    return '\n'.join(lines)


def main(path):
    cells = json.load(open(path))
    grid = generate_grid(cells)
    print(latex_from_grid(grid))

if __name__=='__main__':
    if len(sys.argv)!=2:
        print(f"Usage: {sys.argv[0]} <cells.json>")
        sys.exit(1)
    main(sys.argv[1])
