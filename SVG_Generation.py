from PoissonDiscSampling import bridson
import svgwrite


def generate_svg(r, k, width, height):
    wg = svgwrite.Drawing("Poisson_Disc_Sampling.svg", size=(width, height))  # initialize the "canvas" where we draw
    wg.add(wg.rect(insert=(0, 0), size=('100%', '100%'), rx=None, ry=None, fill='white'))  # draw a white rect
    # that will be used as background
    grid = bridson(r, k, width, height)  # store the sample's grid using the bridson algorithm
    for i in grid:  # for each sample in the background grid
        if i != -1:  # that exist
            wg.add(wg.circle(center=(i.x, i.y), r=1, fill='black'))  # draw a black circle
    wg.save()  # save the svg file


if __name__ == '__main__':
    generate_svg(15, 30, 400, 400)
