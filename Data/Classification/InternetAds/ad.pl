#!/usr/bin/perl
sub readlist();
sub readln();
sub writelist(@);

$BLANK = "";
$COMMA = ",";
$INFILE = "add.csv";
$OUTFILE = "ad.csv";
$TRUE = 1;
$FALSE = 0;

open STDIN, "<", $INFILE || die "Cannot open input dataset $INFILE: $!\n";
open STDOUT, ">", $OUTFILE || die "Cannot open output dataset $OUTFILE: $!\n";

@HEAD = &readlist();
shift @HEAD;
$ncol = @HEAD;
@NAMES = ("height", "width", "aspect_ratio");
for ($i = 3; $i < $ncol; $i++) {push @NAMES, "x" . ($i - 2)}
$NAMES[-1] = "class";
&writelist(@NAMES);


while (!eof(STDIN)) {
  @field = &readlist();
  shift @field;
  for ($i = 0; $i < $ncol; $i++) {if ($field[$i]=~m/\?$/) {$field[$i] = $BLANK}}
  if ($field[-1]=~m/^ad/) {$field[-1] = $TRUE}
  else {$field[-1] = $FALSE}
  &writelist(@field);
}

sub readlist() {
  my $line = &readln;
  return split($COMMA, $line);
}

sub readln() {
  my $line = <STDIN>;
  chomp $line;
  return $line;
}

sub writelist(@) {
  my $line = join($COMMA, @_);
  &writeln($line);
}

sub writeln($) {
  my ($line) = @_;
  print "$line\n";
}
