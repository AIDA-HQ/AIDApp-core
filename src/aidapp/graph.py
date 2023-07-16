"""Graph of the final iteration."""


class Graph:
    """Class that holds all what's needed to plot the final graph."""

    @staticmethod
    def plot_final(
        x_bilinear,
        y_bilinear_ms2,
        sd_meters,
        sa_ms2,
        kn_eff_list,
        figure,
        canvas,
        y_bilinear_ms2_0,
        kn_eff_list_0,
        de_0,
        de_n,
        dp,
    ):
        """
        Function to plot the final graph, meant to be displayed when
        all the curves are calculated in the final iteration.
        """
        # Setup the figure
        figure.clear()
        ax = figure.add_subplot(111)
        canvas.draw()

        # ADRS spectrum
        ax.plot(
            sd_meters, sa_ms2, color="#000000", label=r"$\mathregular{S_e (\xi=5\%)}$"
        )

        # OG Structure
        ax.plot(
            x_bilinear, y_bilinear_ms2_0, color="#FF0000", label="Struttura originale"
        )
        ax.vlines(de_0[0], 0, de_0[1], color="#FF0000", linestyle="dashed")
        ax.plot(
            sd_meters,
            kn_eff_list_0,
            color="#FF0000",
            linestyle="--",
        )

        # Reinforced Structure
        ax.plot(
            x_bilinear, y_bilinear_ms2, color="#00B050", label="Struttura rinforzata"
        )
        ax.vlines(de_n[0], 0, de_n[1], color="#00B050", linestyle="dashed")
        ax.plot(
            sd_meters,
            kn_eff_list,
            color="#00B050",
            linestyle="--",
        )

        # dp
        ax.axvline(x=dp, color="grey", linestyle="dotted")

        # Axis labels
        ax.set_xlabel(r"$\mathregular{S_{De}}$", fontsize=15)
        ax.set_ylabel(r"$\mathregular{S_e}$", fontsize=15)

        # Spine labels
        x = [de_0[0], de_n[0], dp]
        labels = ["$d_e^1$", "$d_e^i$", "$d_p^*$"]
        ax.set_xticks(x, labels)

        # Spine configs
        ax.spines["right"].set_visible(False)
        ax.spines["top"].set_visible(False)

        # Legend
        ax.legend(loc="upper right", framealpha=1, borderpad=1)
