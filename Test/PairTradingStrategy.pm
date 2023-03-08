package PairTradingStrategy;
use Moose;

has [qw(symbol1 symbol2)] => (
    is => 'ro',
    isa => 'Str',
    required => 1,
);

has lookback_period => (
    is => 'ro',
    isa => 'Int',
    required => 1,
);

has zscore_threshold => (
    is => 'ro',
    isa => 'Num',
    required => 1,
);

sub generate_signals {
    my ($self, $data) = @_;

    # Compute the spread between the two securities
    my $spread = $data->{$self->symbol1} - $data->{$self->symbol2};

    # Compute the rolling mean and standard deviation of the spread
    my $spread_mean = $spread->rolling($self->lookback_period)->mean();
    my $spread_std = $spread->rolling($self->lookback_period)->std();

    # Compute the z-score of the current spread value
    my $zscore = ($spread - $spread_mean) / $spread_std;

    # Generate the buy and sell signals based on the z-score
    $data->{'Signal'} = 0;
    $data->where($zscore > $self->zscore_threshold, -1, 'Signal');
    $data->where($zscore < -$self->zscore_threshold, 1, 'Signal');

    return $data;
}

1;
