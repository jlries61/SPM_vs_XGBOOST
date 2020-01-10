#!/usr/bin/perl

use Set::Tiny;

sub dequote(@);
sub getind($%);
sub getval($\@\%);
sub mkindex(@);
sub putval($$\@\%);
sub readlist($);
sub readln($);
sub writelist($@);
sub writeln($$);

$INTRAIN = "train.csv";
$OUTTRAIN = "train_filtered.csv";
@TF = ("VAR_0008", "VAR_0009", "VAR_0010", "VAR_0011", "VAR_0012", "VAR_0043",
       "VAR_0196", "VAR_0226", "VAR_0229", "VAR_0230", "VAR_0232", "VAR_0236",
       "VAR_0239");
$EXCLUDE = Set::Tiny->new("VAR_0075", "VAR_0166", "VAR_0167", "VAR_0168", "VAR_0169",
                          "VAR_0176", "VAR_0177", "VAR_0178", "VAR_0179", "VAR_0200",
                          "VAR_0204", "VAR_0217");
$DLM = ",";

open STDIN, "<", $INTRAIN || die;
open STDOUT, ">", $OUTTRAIN || die;

@INNAMES = &dequote(&readlist(STDIN));
@OUTNAMES = ();
foreach my $name (@INNAMES) {
  if (!$EXCLUDE->has($name)) {push @OUTNAMES, $name}
}
%index = &mkindex(@INNAMES);
%outind = &mkindex(@OUTNAMES);

&writelist(STDOUT, @OUTNAMES);
while (!eof(STDIN)) {
  my @infield = &readlist(STDIN);
  my @outfield;
  foreach my $name (@TF) {
    my $value0 = &getval($name, \@infield, \%index);
    my $value;
    if ($value0 eq "TRUE") {$value = 1}
    elsif ($value eq "FALSE") {$value = 0}
    &putval($name, $value, \@infield, \%index);
  }
  foreach my $name (@OUTNAMES) {
    my $value = &getval($name, \@infield, \%index);
    &putval($name, $value, \@outfield, \%outind);
  }
  &writelist(STDOUT, @outfield);
}

sub dequote(@) {
  my @retval = ();
  foreach my $value (@_) {
    $value =~ s/\"//g;
    push @retval, $value;
  }
  return @retval;
}

sub getind($%) {
  my ($name, %index) = @_;
  my $index = $index{$name};
  if (!defined($index)) {die "Field name $name not found\n"}
  return $index;
}

sub getval($\@\%) {
  my ($name, $pbuf, $pindex) = @_;
  my $index = &getind($name, %$pindex);
  return $$pbuf[$index];
}

sub mkindex(@) {
  my $nf = @name = @_;
  my %index;
  for (my $i = 0; $i < $nf; $i++) {$index{$name[$i]} = $i}
  return %index;
}

sub putval($$\@\%) {
  my ($name, $value, $pbuf, $pindex) = @_;
  my $index = &getind($name, %$pindex);
  $$pbuf[$index] = $value;
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
  my $line = join($ODLM, @list);
  &writeln($fh, $line);
}

sub writeln($$) {
  my ($fh, $line) = @_;
  print $fh "$line\n";
}
