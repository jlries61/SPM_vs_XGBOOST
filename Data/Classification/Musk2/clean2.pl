#!/usr/bin/perl
sub readlist($);
sub readln($);
sub writelist($@);
sub writeln($$);

$DLM = ",";
$INFILE = "clean2.data";
$OUTFILE = "clean2.csv";
$NF = 166;

open STDIN, "<", $INFILE || die "Failure to open input file $INFILE: $!\n";
open STDOUT, ">", $OUTFILE || die "Failure to open output file $OUTFILE: $!\n";

@NAMES = ();
for (my $i = 1; $i <= $NF; $i++) {push @NAMES, "f" . $i}
push @NAMES, "class";
&writelist(STDOUT, @NAMES);

while (!eof(STDIN)) {
  my @fields = &readlist(STDIN);
  for (my $i = 0; $i < 2; $i++) {shift @fields}
  &writelist(STDOUT, @fields)
}

sub readlist($) {
  my ($fh) = @_;
  my $line = &readln($fh);
  return split($DLM, $line);
}

sub readln($) {
  my ($fh) = @_;
  my $line = <$fh>;
  chomp $line;
  return $line;
}

sub writelist($@) {
  my ($fh, @list) = @_;
  &writeln($fh, join($DLM, @list));
}

sub writeln($$) {
  my ($fh, $line) = @_;
  print $fh "$line\n";
}
